# Fluent Transfer

Fluent Transfer is a desktop GUI prototype for audio/video transcription and subtitle translation. It was originally built as a university graduation project, so the codebase is more of an experimental demo than a polished production application.

The underlying transcription and translation flow is based on an OpenLRC-style pipeline: audio preprocessing, Whisper/faster-whisper transcription, subtitle optimization, and optional LLM-based translation. This project mainly adds a PySide6 desktop interface on top of that workflow.

The GUI is built with PyQt-Fluent-Widgets (`qfluentwidgets`) and follows Microsoft's Fluent UI design ideas, including a navigation sidebar, card-style settings, theme switching, and a simple library view for generated subtitle records.

## Tech Stack

- Python
- PySide6 / Qt
- PyQt-Fluent-Widgets (`qfluentwidgets`)
- OpenLRC-style subtitle generation pipeline
- faster-whisper
- MySQL / PyMySQL for local subtitle history

## Running Locally

This project does not include a polished installer. To run it locally, prepare the required Python dependencies and start the app with:

```bash
python main.py
```

You may also need FFmpeg, faster-whisper runtime/model dependencies, LLM API credentials for translation, and a local MySQL database named `fluent_transfer1` with a `file_records` table.

Some local environment settings are still hard-coded in the prototype, so setup may require manual adjustment.

## Related Projects

- [OpenLRC](https://github.com/zh-plus/openlrc)
- [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
