# IMD Swarm Field Guide

The requested one-hour video is **[artifacts/video.mp4](artifacts/video.mp4)** (`video/mp4`). It teaches how to choose and describe requests at [explorer.imd.fun/launch](https://explorer.imd.fun/launch), then follows illustrative checks, handoffs, failures and revisions.

The film contains 120 distinct 30-second scenes. Each chapter lasts five minutes. The MP4 includes chapter markers. A complete [transcript](TRANSCRIPT.md) provides scene timestamps and the spoken text.

| Start | Chapter |
| --- | --- |
| 00:00 | Start here: choose, describe, check and pay |
| 05:00 | Launch a company |
| 10:00 | Ask the oracle |
| 15:00 | Heartbeat preview — currently Soon |
| 20:00 | Token |
| 25:00 | Contracts: launch versus source-only draft |
| 30:00 | v4 hook |
| 35:00 | Audit |
| 40:00 | Report |
| 45:00 | Website |
| 50:00 | Image and Audio |
| 55:00 | Video and final practice |

## Media specification

- Duration: **3,600 seconds / 60:00**.
- Dimensions: **1280 × 720**, 16:9.
- Video: **H.264**, `yuv420p`, 5 frames per second, with a progress indicator changing every five seconds. Original teaching cards hold for thirty seconds each.
- Audio: **AAC**, mono, 22,050 Hz, nominal 48 kbit/s. Synthetic English narration from the bundled meSpeak voice. No music. Approximately 44.78 minutes of spoken content; the rest is deliberate reading and reflection time within each scene.
- MP4 streaming: `+faststart`; the `moov` atom precedes media data.
- File size: **27,424,189 bytes (26.15 MiB)**, below 64 MiB. Exact bytes, SHA-256, codecs, streams and chapter timing are in [source/verification.json](source/verification.json).

## Scope and limitations

This is a narrated educational simulation using original text cards, not a screen recording or generated cinematic footage. Fictional Repair Club briefs and outcomes are explicitly labeled. No paid requests, wallet signatures, deployed contracts, token launches, Oracle signatures or schedules were created. No invented fees or addresses are presented as real records. Work stages are compressed teaching examples, not predictions of service latency or guarantees of results.

The launch page was read on **2026-10-04**. Every visible request tile is covered. Heartbeat was disabled and marked **Soon**; its chapter is a planning preview. The company form offered Sepolia while Ethereum mainnet, Base and Robinhood Chain were marked soon. Public client strings supply additional route descriptions and declared output formats; they are not evidence that hidden or upcoming features are enabled. Availability and product behavior can change. [Saved references and direct quotations](source/reference/README.md) document the source snapshot.

Synthetic narration can mispronounce names, abbreviations and code identifiers. The transcript gives their exact spelling. The film contains no embedded closed-caption track; its companion transcript is readable independently. Visual checks inspect rendered frames; signal and decoding checks do not constitute a human listening review or a certification of instruction quality. The video demonstrates how to specify and review outcomes, but does not execute or validate the fictional contracts, audits, research reports or media described in the scenarios.

## Local checks and reproduction

Run `PYTHONDONTWRITEBYTECODE=1 python3 source/build.py` to rebuild with Python 3.12, Node and ffmpeg. Fonts, Pillow and the speech engine are bundled as ordinary files; the build needs no network. See [dependency details and licenses](source/DEPENDENCIES.md). Temporary images and uncompressed audio are confined to `/tmp`.

Run `PYTHONDONTWRITEBYTECODE=1 python3 source/verify.py` to check codecs, pixel format, dimensions, duration, twelve chapters, size and MP4 atom order; decode the complete video and audio; measure audio levels; and generate a twelve-chapter [contact sheet](source/preview.jpg). [Verification evidence](source/verification.json) records the results. These checks establish file structure and decodability, not the truth of simulated outcomes or the behavior of the live service.

The named MP4 output is left untracked for separate upload.

Bundle repair: removed duplicate Python 3.11 Pillow binaries and unused AVIF binaries while retaining the Python 3.12 rendering dependencies, speech engine, fonts and licenses. A complete offline rebuild succeeded after trimming. A gzip-compressed tar of the retained tracked source files measures approximately 6.05 MiB, below the 8 MiB upload limit; the named MP4 is delivered separately.
