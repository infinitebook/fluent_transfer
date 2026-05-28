# Fluent Transfer

Fluent Transfer is a desktop subtitle transcription and translation tool built as a graduation project prototype. It wraps an OpenLRC-based transcription/translation pipeline with a modern PySide6 GUI inspired by Microsoft's Fluent UI design language.

The project focuses on making audio and video subtitle generation easier to use: select a media file, choose a target language, start the task from the GUI, and manage the generated subtitle files from the built-in library view.

## Highlights

- Audio/video transcription powered by a local OpenLRC-style `LRCer` pipeline
- Optional subtitle translation to the selected target language
- `.lrc` subtitle output for audio files and `.srt` subtitle output for video files
- Fluent-style desktop interface built with PySide6 and PyQt-Fluent-Widgets / `qfluentwidgets`
- Home, library, and settings pages using a Microsoft Fluent UI-inspired layout
- Subtitle history management backed by a local MySQL database
- Configurable default output folder
- Light/dark/system theme support and Windows 11 Mica effect support where available

## Project Background

This repository was originally developed as a university graduation project. The core idea was to turn the powerful but developer-oriented OpenLRC workflow into a more approachable desktop application.

OpenLRC provides the underlying speech-to-subtitle workflow: audio preprocessing, Whisper/faster-whisper transcription, subtitle optimization, and LLM-based translation. Fluent Transfer adds a GUI layer on top of that workflow so users can operate the pipeline through a familiar desktop interface instead of running scripts manually.

The UI is built around the Fluent Design style: a clean navigation sidebar, card-based settings, soft visual hierarchy, theme switching, and desktop-native interaction patterns.

## Tech Stack

- Python
- PySide6 / Qt for the desktop application shell
- PyQt-Fluent-Widgets (`qfluentwidgets`) for Fluent-style components
- OpenLRC-inspired subtitle generation pipeline
- faster-whisper for speech recognition
- LLM-based translation support
- MySQL / PyMySQL for local subtitle record management

## Basic Workflow

1. Open Fluent Transfer.
2. Select an audio or video file from the home page.
3. Choose the target language.
4. Choose whether to translate the transcription result.
5. Start the task and wait for the progress indicator to finish.
6. Find the generated subtitle file in the source directory or configured default output folder.
7. Review previous subtitle files from the library page.

## Supported Target Languages

The GUI currently exposes these target language options:

- Simplified Chinese (`zh-hans`)
- Traditional Chinese (`zh-hant`)
- English (`en`)
- Japanese (`ja`)
- Korean (`ko`)
- French (`fr`)
- Russian (`ru`)
- German (`de`)

## Running Locally

This is an early prototype and does not yet include a polished installer. To run it locally, prepare a Python environment with the required GUI, transcription, translation, and database dependencies, then start the application with:

```bash
python main.py
```

You may also need to prepare:

- FFmpeg, for audio extraction from video files
- model/runtime dependencies required by faster-whisper
- API credentials for the configured LLM translation provider
- a local MySQL database named `fluent_transfer1` with a `file_records` table for subtitle history

## Notes

- This repository is a preserved graduation-project codebase, so some environment assumptions are still hard-coded in the prototype.
- The current database settings are local-development defaults and should be changed before real deployment.
- The project is mainly useful as a GUI experiment around OpenLRC-style subtitle workflows and Fluent-style Python desktop application design.

## Related Projects

- [OpenLRC](https://github.com/zh-plus/openlrc) - transcription and translation pipeline for generating LRC subtitles
- [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) - Fluent Design component library for Python Qt applications

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
