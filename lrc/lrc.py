

import concurrent.futures
import json
import shutil
from pathlib import Path
from pprint import pformat
from queue import Queue
from threading import Lock
from typing import List

from faster_whisper.transcribe import Segment

from lrc.context import Context
from lrc.defaults import default_asr_options, default_vad_options, default_preprocess_options
from lrc.logger import logger
from lrc.opt import SubtitleOptimizer
from lrc.preprocess import Preprocessor
from lrc.subtitle import Subtitle, BilingualSubtitle
from lrc.transcribe import Transcriber
from lrc.translate import LLMTranslator
from lrc.utils import Timer, extend_filename, get_audio_duration, format_timestamp, extract_audio, \
    get_file_type

from PySide6.QtCore import QObject, Signal, Slot


class LRCer:
    """
    Args:
        whisper_model: Name of whisper model (tiny, tiny.en, base, base.en, small, small.en, medium,
            medium.en, large-v1, large-v2, large-v3, distill-large-v3) When a size is configured,
            the converted model is downloaded from the Hugging Face Hub. Default: ``large-v3``
        compute_type: The type of computation to use. Can be ``int8``, ``int8_float16``, ``int16``,
            ``float16`` or ``float32``. Default: ``float16``
        chatbot_model: The chatbot model to use, currently we support gptbot from , claudebot from Anthropic.
            OpenAI: gpt-4-0125-preview, gpt-4-turbo-preview, gpt-3.5-turbo-0125, gpt-3.5-turbo
            Anthropic: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
            Default: ``gpt-3.5-turbo``
        fee_limit: The maximum fee you are willing to pay for one translation call. Default: ``0.1``
        consumer_thread: To prevent exceeding the RPM and TPM limits set by OpenAI, the default is TPM/MAX_TOKEN.
        asr_options: Parameters for whisper model.
        vad_options: Parameters for VAD model.
        proxy: Proxy for openai requests. e.g. 'http://127.0.0.1:7890'
    """
    def __init__(self, whisper_model='large-v3', compute_type='float16', chatbot_model: str = 'gpt-3.5-turbo',
                 fee_limit=0.1, consumer_thread=4, asr_options=None, vad_options=None, preprocess_options=None,
                 proxy=None):

        self.chatbot_model = chatbot_model
        self.fee_limit = fee_limit
        self.api_fee = 0  # Can be updated in different thread, operation should be thread-safe
        self.from_video = set()
        self.context: Context = Context()
        self.proxy = proxy

        self._lock = Lock()
        self.exception = None
        self.consumer_thread = consumer_thread

        # Default Automatic Speech Recognition (ASR) options
        self.asr_options = default_asr_options

        # Parameters for VAD (see faster_whisper.vad.VadOptions), tune them if speech is not being detected
        self.vad_options = default_vad_options

        self.preprocess_options = default_preprocess_options

        if asr_options:
            self.asr_options.update(asr_options)

        if vad_options:
            self.vad_options.update(vad_options)

        if preprocess_options:
            self.preprocess_options.update(preprocess_options)

        self.transcriber = Transcriber(model_name=whisper_model, compute_type=compute_type,
                                       asr_options=self.asr_options, vad_options=self.vad_options)
        self.transcribed_paths = []

    def transcription_producer(self, transcription_queue, audio_paths, src_lang):
        """
        Sequential Producer.
        """
        for audio_path in audio_paths:
            transcribed_path = extend_filename(audio_path, '_transcribed').with_suffix('.json')
            if not transcribed_path.exists():
                with Timer('Transcription process'):
                    logger.info(
                        f'Audio length: {audio_path}: {format_timestamp(get_audio_duration(audio_path), fmt="srt")}')
                    segments, info = self.transcriber.transcribe(audio_path, language=src_lang)
                    logger.info(f'Detected language: {info.language}')

                    # [Segment(start, end, text, words=[Word(start, end, word, probability)])]

                # Save the transcribed json
                self.to_json(segments, name=transcribed_path, lang=info.language)  # xxx_transcribed.json
            else:
                logger.info(f'Found transcribed json file: {transcribed_path}')
            transcription_queue.put(transcribed_path)
            # logger.info(f'Put transcription: {transcribed_path}')

        transcription_queue.put(None)
        logger.info('Transcription producer finished.')

    def transcription_consumer(self, transcription_queue, target_lang, prompter, skip_trans, bilingual_sub):
        """
        Parallel Consumer.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.consumer_worker, transcription_queue, target_lang, prompter, skip_trans,
                                       bilingual_sub)
                       for _ in range(self.consumer_thread)]
            concurrent.futures.wait(futures)
        logger.info('Transcription consumer finished.')

    def consumer_worker(self, transcription_queue, target_lang, prompter, skip_trans, bilingual_sub):
        """
        Parallel translation.
        """
        while True:
            logger.debug(f'Translation worker waiting transcription...')
            transcribed_path = transcription_queue.get()

            if transcribed_path is None:
                transcription_queue.put(None)
                logger.debug('Translation worker finished.')
                return

            logger.info(f'Got transcription: {transcribed_path}')
            transcribed_sub = Subtitle.from_json(transcribed_path)
            transcribed_opt_sub = self.post_process(transcribed_sub, update_name=True)
            audio_name = transcribed_path.stem.replace('_transcribed', '')

            # xxx_transcribed_optimized_translated.json
            translated_path = extend_filename(transcribed_opt_sub.filename, '_translated')

            final_json_path = Path(translated_path.parent / f'{audio_name}.json')
            if final_json_path.exists():
                final_subtitle = Subtitle.from_json(final_json_path)
            elif skip_trans:
                shutil.copy(transcribed_opt_sub.filename, final_json_path)
                final_subtitle = transcribed_opt_sub
                final_subtitle.filename = final_json_path
            else:
                with Timer('Translation process'):
                    try:
                        final_subtitle = self._translate(audio_name, prompter, target_lang, transcribed_opt_sub,
                                                         translated_path)
                    except Exception as e:
                        self.exception = e
                        return

            # Copy preprocessed/xxx_preprocessed.lrc or preprocessed/xxx_preprocessed.srt to xxx.lrc or xxx.srt
            if audio_name in self.from_video:
                subtitle_path = final_subtitle.to_srt()
            else:
                subtitle_path = final_subtitle.to_lrc()

            suffix = subtitle_path.suffix
            result_path = subtitle_path.parents[1] / subtitle_path.name.replace(f'_preprocessed{suffix}',
                                                                                suffix)
            shutil.copy(subtitle_path, result_path)

            # Bilingual
            if bilingual_sub:
                bilingual_subtitle = BilingualSubtitle.from_preprocessed(transcribed_path.parent,
                                                                         audio_name.replace('_preprocessed', ''))
                bilingual_subtitle.to_lrc()
                bilingual_lrc_path = bilingual_subtitle.filename.with_suffix(bilingual_subtitle.suffix)
                shutil.copy(bilingual_lrc_path, result_path.parent / bilingual_lrc_path.name)

            logger.info(f'Translation fee til now: {self.api_fee:.4f} USD')

            self.transcribed_paths.append(result_path)

    def _translate(self, audio_name, prompter, target_lang, transcribed_opt_sub, translated_path):
        json_filename = Path(translated_path.parent / (audio_name + '.json'))
        compare_path = Path(translated_path.parent, f'{audio_name}_compare.json')
        if not translated_path.exists():
            # Translate the transcribed json
            translator = LLMTranslator(chatbot_model=self.chatbot_model, prompter=prompter, fee_limit=self.fee_limit,
                                       proxy=self.proxy)
            context = self.context

            target_texts = translator.translate(
                transcribed_opt_sub.texts,
                src_lang=transcribed_opt_sub.lang,
                target_lang=target_lang,
                title=audio_name,
                audio_type=context.audio_type,
                background=context.background,
                description=context.get_description(audio_name),
                compare_path=compare_path
            )

            with self._lock:
                self.api_fee += translator.api_fee  # Ensure thread-safe

            transcribed_opt_sub.set_texts(target_texts, lang=target_lang)

            # xxx_transcribed_optimized_translated.json
            transcribed_opt_sub.save(translated_path, update_name=True)
        else:
            logger.info(f'Found translated json file: {translated_path}')
        translated_sub = Subtitle.from_json(translated_path)

        final_subtitle = self.post_process(translated_sub, output_name=json_filename, update_name=True)  # xxx.json

        return final_subtitle

    def run(self, paths, src_lang=None, target_lang='zh-cn', prompter='base_trans', context_path=None,
            skip_trans=False, noise_suppress=False, bilingual_sub=False, clear_temp_folder=False) -> List[str]:
        """
        Split the translation into 2 phases: transcription and translation. They're running in parallel.
        Firstly, transcribe the audios one-by-one. At the same time, translation threads are created and waiting for
        the transcription results. After all the transcriptions are done, the translation threads will start to
        translate the transcribed texts.

        Args:
            paths (Union[str, Path, List[Union[str, Path]]]): Audio/Video paths, can be a list or a single path.
            src_lang (str): Language of the audio, default to auto-detect.
            target_lang (str): Target language, default to Mandarin Chinese.
            prompter (str): Currently, only `base_trans` is supported.
            context_path (str): path to context config file. (Default to use `context.yaml` in the first audio's directory)
            skip_trans (bool): Whether to skip the translation process. (Default to False)
            noise_suppress (bool): Whether to suppress the noise in the audio. (Default to False)
            bilingual_sub (bool): Whether to generate bilingual subtitles. (Default to False)
            clear_temp_folder (bool): Whether to clear the temporary folder.
                Note, set this back to False to see more intermediate results if error encountered. (Default to False)

        Returns:
            List[str]: List of paths to the transcribed files.

        Raises:
            Exception: If an exception occurs during the transcription or translation process.
        """
        self.transcribed_paths = []

        if not paths:
            logger.warning('No audio/video file given. Skip LRCer.run()')
            return []

        if isinstance(paths, str) or isinstance(paths, Path):
            paths = [paths]

        paths = list(map(Path, paths))

        if context_path:
            context_path = Path(context_path)
            self.context.load_config(context_path)
            logger.info(f'Found context config: {context_path}')
            logger.debug(f'Context: {self.context}')
        else:
            # Try to find the default `context.yaml` in the first audio's directory
            try:
                context_path = paths[0].parent / 'context.yaml'
                self.context.load_config(context_path)
                logger.info(f'Found context config file: {context_path}')
            except FileNotFoundError:
                logger.info(f'Default context config not found: {self.context}, using default context.')

        audio_paths = self.pre_process(paths, noise_suppress=noise_suppress)

        logger.info(f'Working on {len(audio_paths)} audio files: {pformat(audio_paths)}')

        transcription_queue = Queue()

        with Timer('Transcription (Producer) and Translation (Consumer) process'):
            consumer = concurrent.futures.ThreadPoolExecutor(thread_name_prefix='Consumer') \
                .submit(self.transcription_consumer, transcription_queue, target_lang, prompter, skip_trans,
                        bilingual_sub)
            producer = concurrent.futures.ThreadPoolExecutor(thread_name_prefix='Producer') \
                .submit(self.transcription_producer, transcription_queue, audio_paths, src_lang)

            producer.result()
            consumer.result()

            if self.exception:
                # traceback.print_exception(type(self.exception), self.exception, self.exception.__traceback__)
                raise self.exception

        logger.info(f'Totally used API fee: {self.api_fee:.4f} USD')

        if clear_temp_folder:
            logger.info('Clearing temporary folder...')
            self.clear_temp_files(audio_paths)



    @staticmethod
    def clear_temp_files(paths):
        """
        Clear the temporary files generated during the transcription and translation process.
        """
        temp_folders = set([path.parent for path in paths])
        for folder in temp_folders:
            assert folder.name == 'preprocessed', f'Not a temporary folder: {folder}'

            shutil.rmtree(folder)
            logger.debug(f'Removed {folder}')

    @staticmethod
    def to_json(segments: List[Segment], name, lang):
        result = {
            'language': lang,
            'segments': []
        }

        for segment in segments:
            result['segments'].append({
                'start': segment.start,
                'end': segment.end,
                'text': segment.text
            })

        with open(name, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logger.info(f'File saved to {name}')

        return result

    def pre_process(self, paths, noise_suppress=False):
        paths = [Path(path) for path in paths]

        # Check if path is audio or video
        for i, path in enumerate(paths):
            if not path.exists() or not path.is_file():
                raise FileNotFoundError(f'File not found: {path}')

            paths[i] = extract_audio(path)

            if get_file_type(path) == 'video':
                self.from_video.add(path.stem + '_preprocessed')

        # Audio-based process
        preprocessor = Preprocessor(paths, options=self.preprocess_options)
        paths = preprocessor.run(noise_suppress)

        return paths

    @staticmethod
    def post_process(transcribed_sub: Path, output_name: Path = None, remove_files: List[Path] = None,
                     update_name=False):
        optimizer = SubtitleOptimizer(transcribed_sub)
        optimizer.perform_all()
        optimizer.save(output_name, update_name=update_name)

        # Remove intermediate files
        if remove_files:
            _ = [file.unlink() for file in remove_files if file.is_file()]

        return optimizer.subtitle
