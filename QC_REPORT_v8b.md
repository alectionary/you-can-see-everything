# QC REPORT — v8b focused re-check

Reviewed 2026-10-18. **Overall verdict: FAIL.** The requested picture samples, audio checks and regressions pass, but an unscheduled scene-change event remains at 34.000000s. Review only: no media, source, subtitle, score or build files were modified. This report is the sole project output.

| Item | Result | Evidence |
|---|---|---|
| 1a. No >5 event in 33.9–34.5s except exactly 34.5s | **FAIL** | Frame 816, 34.000000s: score **10.126**. Intended frame 828, 34.500000s: score **18.293**. Previous 34.041667s event is now only 1.147, but a different disallowed event occurs one frame earlier. |
| 1b. No unexplained >5 events across final | **FAIL** | Of 33 events above 5, 32 match EDIT_PLAN.md boundaries within one frame; 34.000000s is the sole unmatched event, 12 frames before 34.5s. |
| 2a. Roy at 25s | PASS | Frame 600 shows Roy's face and visible crutches at the right edge of the right panel; full source framing appears over dark blurred padding. |
| 2b. Roy at 28.5s | PASS | Frame 684 shows Roy's face and crutches in the right panel, with demolition in the left. |
| 2c. Dan at 34.25s | PASS | Frame 822 shows Dan in the dominant left two-thirds, Fielder cropped in the right third. |
| 3a. Dialogue/score separation, 45–46.161s | PASS | Dialogue −23.013016 dBFS; score −30.061500 dBFS; difference **+7.048483 dB**, exceeding the 5dB minimum. |
| 3b. Exact PCM silence, 55–56s | PASS | All 48,000 samples are exactly zero; nonzero count 0. Sample indices 2,640,000–2,687,999 inclusive at 48kHz. |
| 3c. Title audio onset | PASS | First PCM sample exceeding −50dBFS at/after 56s is index 2,688,097, **56.002020833s**, +2.021ms from target, within ±10ms. |
| 3d. Rising PCM mix arc | PASS | Requested consecutive windows measure −27.810, −25.575, −23.440, −20.783, −13.847 dBFS; each rises. |
| 4a. Final technical properties | PASS | ffprobe decoded 1,440 frames; video and container duration 60.000000s; 1920×1080; nominal and average frame rates both 24/1. |
| 4b. SRT unchanged from v7 | PASS | Both files have identical bytes and SHA-256 shown below. |
| 4c. 54.5s card | PASS | Frame 1308 reads THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE, exactly four lines. |
| 4d. 57s title | PASS | Frame 1368 reads YOU CAN SEE ANYTHING. |

## Measurement method

Scanned the delivered `you-can-see-anything-teaser-v8.mp4` using:

```sh
ffmpeg -hide_banner -loglevel error -i you-can-see-anything-teaser-v8.mp4 -vf 'scdet=threshold=0.4,metadata=print:file=/tmp/qcv8b/scdet.txt' -an -f null -
```

Compared every `lavfi.scd.score > 5` with the EDIT_PLAN.md union of picture, insert, collage, card, black and title boundaries, allowing ±1 frame (1/24s). Boundary list in seconds:

`0, 4.5, 5.75, 6, 7.5, 10, 12.5, 14, 14.5, 17.5, 20.5, 21.75, 22, 27.25, 29.75, 30, 30.5, 31.75, 34.5, 40, 41.75, 42, 47, 48, 49.75, 50, 50.5, 51.75, 52.5, 53.5, 54, 55, 56, 60`.

The event at 30.041667s remains within the permitted one-frame tolerance of 30s. A title boundary need not produce a >5 score to satisfy this scan; the title is verified visually separately.

Audio uses the supplied native WAV samples, normalized according to sample format. Mean level is whole-window RMS expressed as `20 log10(sqrt(mean(samples²)))`, including pauses, over start-inclusive/end-exclusive windows. The separation window is exactly 45.000–46.161s, not the previous shorter 45–46.1s window. Title onset uses the prior QC's −50dBFS absolute-sample threshold. These are objective measurements, not a subjective masking assessment.

| PCM mix window (s) | RMS dBFS |
|---|---:|
| 0–10 | -27.810084 |
| 20–28 | -25.575183 |
| 32–40 | -23.440274 |
| 42–48 | -20.783117 |
| 50–54 | -13.847221 |

SRT SHA-256 (both v7 and v8):

`5b2c8806b9eadd6363f3d7a9140fac2ab18a1351ba9b4d8434da782d6f59db06`

## All scene-change events scoring above 5

| Time (s) | Frame (zero-based) | Score | Boundary check |
|---:|---:|---:|---|
| 4.500000 | 108 | 27.845 | PASS |
| 5.750000 | 138 | 28.328 | PASS |
| 6.000000 | 144 | 26.399 | PASS |
| 7.500000 | 180 | 24.283 | PASS |
| 10.000000 | 240 | 23.059 | PASS |
| 12.500000 | 300 | 21.689 | PASS |
| 14.000000 | 336 | 15.241 | PASS |
| 14.500000 | 348 | 17.592 | PASS |
| 17.500000 | 420 | 17.640 | PASS |
| 20.500000 | 492 | 31.776 | PASS |
| 21.750000 | 522 | 32.920 | PASS |
| 22.000000 | 528 | 21.649 | PASS |
| 27.250000 | 654 | 9.465 | PASS |
| 29.750000 | 714 | 9.211 | PASS |
| 30.000000 | 720 | 22.530 | PASS |
| 30.041667 | 721 | 9.514 | PASS |
| 30.500000 | 732 | 27.193 | PASS |
| 31.750000 | 762 | 27.379 | PASS |
| 34.000000 | 816 | 10.126 | **FAIL** |
| 34.500000 | 828 | 18.293 | PASS |
| 40.000000 | 960 | 33.012 | PASS |
| 41.750000 | 1002 | 35.128 | PASS |
| 42.000000 | 1008 | 10.408 | PASS |
| 47.000000 | 1128 | 19.001 | PASS |
| 48.000000 | 1152 | 30.090 | PASS |
| 49.750000 | 1194 | 31.653 | PASS |
| 50.000000 | 1200 | 17.054 | PASS |
| 50.500000 | 1212 | 30.876 | PASS |
| 51.750000 | 1242 | 31.259 | PASS |
| 52.500000 | 1260 | 31.186 | PASS |
| 53.500000 | 1284 | 33.068 | PASS |
| 54.000000 | 1296 | 32.604 | PASS |
| 55.000000 | 1320 | 33.768 | PASS |

## Review artifacts

Scratch evidence is in `/tmp/qcv8b/`: detector metadata, complete event JSON, ffprobe JSON, audio measurements, and extracted PNGs at 25, 28.5, 34.25, 54.5 and 57s, plus `frames.jpg`. Frames were read directly from the final MP4. No rebuild or correction was performed.
