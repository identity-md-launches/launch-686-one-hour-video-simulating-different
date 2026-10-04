# Offline production dependencies

The build uses Python 3.12 and Node to render original cards and synthesize speech, then calls the host's ffmpeg. No network is used by `build.py`. The task environment already provided ffmpeg and Node.

Bundled ordinary files:

- Pillow 11.3.0 CPython 3.12 Linux x86_64 wheel, expanded under `vendor/`. Original metadata, license files and bundled-library notices are preserved. Duplicate CPython 3.11 binaries and the unused AVIF extension/library are omitted; the PNG/JPEG card and preview workflow uses the retained CPython 3.12 rendering and font libraries. The wheel metadata describes the original distribution, so its RECORD also lists omitted files. Download: https://pypi.org/project/pillow/11.3.0/
- meSpeak 2.0.2 from https://registry.npmjs.org/mespeak/-/mespeak-2.0.2.tgz, expanded under `vendor/mespeak/package/`. Original JS source, voice data and documentation are preserved. This project is GPL licensed and based on eSpeak/speak.js. See the bundled documentation and GPL text.
- Liberation Sans regular and bold, copied from the runtime's fonts with their original copyright/license notice in `fonts/LICENSE`.

Rebuild command from the repository root: `PYTHONDONTWRITEBYTECODE=1 python3 source/build.py`.

Temporary cards and uncompressed audio are created only under a temporary directory in `/tmp` and automatically removed after a successful build. meSpeak runs once per process because its older Emscripten runtime does not reliably support repeated long utterances in this Node runtime. Speech longer than 28 seconds is compressed to 27.5 seconds with ffmpeg atempo; the rest of each 30-second scene is a reading pause.
