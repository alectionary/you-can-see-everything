# QC REPORT — v9 focused review

Reviewed 2026-10-18 against the **v9 revision** section of EDIT_PLAN.md and the prior v8/v8b reports. **Overall verdict: PASS.** All requested checks pass. No media, source, subtitle or build files were changed; this report is the sole project output.

| Item | Result | Evidence |
|---|---|---|
| 1. Card 8 at 54.2s and 55.2s; black by 55.75s | PASS | Both requested instants show exactly four lines: THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE. Frame 1338 at 55.750000s is pure black: every decoded RGB channel has minimum and maximum 0. |
| 2. Closing title at 57s | PASS | Frame 1368 reads exactly YOU CAN SEE EVERYTHING, with no additional words. |
| 3a. PCM silence, 55.000–56.000s | PASS | Native 48kHz signed 16-bit mono master: samples 2,640,000–2,687,999 inclusive are exactly zero; 0 nonzero samples out of 48,000. |
| 3b. Title audio onset, 56.000s ±0.010s | PASS | First nonzero sample is 2,688,000 at exactly 56.000000s. First absolute sample above −50dBFS is 2,688,097 at 56.002020833s (+2.021ms), also within tolerance. |
| 3c. Rising PCM mix arc | PASS | Consecutive whole-window RMS levels are −27.810084, −25.575183, −23.440274, −20.783117 and −13.847221 dBFS; every window rises. |
| 4. Scene-change scan | PASS | All 31 events scoring strictly above 5 match the revised boundary list within one frame. No unmatched events. The prior v8b 34.000000s failure does not recur above 5. |
| 5a. Duration / frames / dimensions / rate | PASS | Container, video and audio durations are 60.000000s; 1,440 declared and decoded video frames; 1920×1080; nominal and average frame rates both 24/1. |
| 5b. SRT unchanged | PASS | build/v9/teaser.srt and build/v7/teaser.srt are byte-identical, 705 bytes each. |
| 5c. Roy at 25s | PASS | Frame 600 shows Roy in the right panel with visible crutches at its right edge, retaining the padded source framing. |
| 5d. Dan at 34.25s | PASS | Frame 822 shows Dan dominant in the left two-thirds, with Fielder cropped in the right third. |

## Frame and audio methods

Frames were decoded directly from you-can-see-anything-teaser-v9.mp4 and inspected visually. At 24fps, the frames displayed at 54.2s and 55.2s are zero-based frames 1300 and 1324, whose presentation times are 54.166667s and 55.166667s; each remains displayed through the requested instant. The 55.75s black check additionally measured all pixels of the decoded PNG.

Audio measurements use build/v9/audio_mix.wav directly: 48,000Hz, mono, 16-bit PCM, 2,880,000 samples (60s). Intervals are start-inclusive/end-exclusive. RMS is 20 log10(sqrt(mean(normalized samples²))), including pauses. These are objective checks of the requested mix arc and onset, not a subjective listening assessment.

| PCM window (s) | RMS dBFS |
|---|---:|
| 0–10 | -27.810084 |
| 20–28 | -25.575183 |
| 32–40 | -23.440274 |
| 42–48 | -20.783117 |
| 50–54 | -13.847221 |

SRT SHA-256 (both files): `5b2c8806b9eadd6363f3d7a9140fac2ab18a1351ba9b4d8434da782d6f59db06`.

## Scene-change evidence

Command used on the final MP4:

```sh
ffmpeg -hide_banner -loglevel error -i you-can-see-anything-teaser-v9.mp4 -vf 'scdet=threshold=0.4,metadata=print:file=/tmp/qcv9/scdet.txt' -an -f null -
```

Revised allowed boundaries (seconds), replacing 55 with 55.5 as specified:

`0, 4.5, 5.75, 6, 7.5, 10, 12.5, 14, 14.5, 17.5, 20.5, 21.75, 22, 27.25, 29.75, 30, 30.5, 31.75, 34.5, 40, 41.75, 42, 47, 48, 49.75, 50, 50.5, 51.75, 52.5, 53.5, 54, 55.5, 56, 60`.

Tolerance is ±1 frame (1/24s). The event at 30.041667s is within one frame of 30s. A planned boundary need not generate a score above 5; this test checks for unexpected above-5 events.

| Time (s) | Frame (zero-based) | Score | Result |
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
| 31.750000 | 762 | 32.912 | PASS |
| 34.500000 | 828 | 18.306 | PASS |
| 40.000000 | 960 | 33.009 | PASS |
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
| 54.000000 | 1296 | 32.603 | PASS |

Scratch evidence is retained in /tmp/qcv9/: ffprobe JSON, detector metadata, event JSON, PCM measurements, six extracted PNGs and a contact sheet. No rebuild or correction was performed.
