# QC report — teaser v7

Reviewed 2026-10-18. Review only: no media, build, dialogue, subtitle, or reference documents changed. Reviewed `you-can-see-anything-teaser-v7.mp4` against the current SCRIPT.md, PACING_NOTES.md, MUSIC_CUES.md, build/build_teaser_v7.sh, build/v7/teaser.srt, the eleven specified dialogue/v2 MP3s, and ../dan-and-roy-parking/CHARACTER_BIBLE.md.

## Overall verdict — FAIL (strict timing/document compliance)

The two stray clip heads are fixed. Subtitle text and timing, Fielder pitch, requested music levels, technical delivery, and all eight requested frame samples pass. No new unscheduled scene change above score 5 was found. However, five intended cuts land one frame (0.041667s) late, outside their exact scheduled timestamps. The title also appears one frame late. Current PACING_NOTES.md still requires silence under the title, contradicting MUSIC_CUES.md and the delivered title note. These are the remaining exceptions; no fixes were made.

## 1. Technical — PASS

ffprobe: container, video, and audio durations each **60.000000s**; **1920×1080**, H.264, nominal and average frame rate **24/1**, **1,440 frames**. Audio present: AAC LC, **48,000Hz, mono**.

## 2. Cuts — FAIL for exact scheduled timing; clip-head fixes PASS

Ran FFmpeg on the final at native resolution with `scdet=threshold=0.4,metadata=print`. Scores below use scdet's 0–100 scale; metadata was collected for every frame. There are 73 events at or above 0.4. All events above 5 are listed below. None is a subtitle boundary; the delayed events correspond to intended scene transitions, not additional stray takes.

| Scheduled cut (s) | Measured event (s) | Score | Result |
|---:|---:|---:|---|
| 6 | 6.000000 | 18.563 | PASS |
| 14 | 14.000000 | 15.236 | PASS |
| 22 | 22.000000 | 19.923 | PASS |
| 30 | 30.041667 | 16.420 | FAIL: one frame late |
| 34 | 34.041667 | 21.187 | FAIL: one frame late |
| 40 | 40.041667 | 17.293 | FAIL: one frame late |
| 42 | 42.041667 | 6.868 | FAIL: one frame late |
| 55 | 55.041667 | 32.677 | FAIL: one frame late |
| 56 | 56.041667 | 0.368 | FAIL: title one frame late; below detection threshold |

The title event is visible in the all-frame metadata despite falling below 0.4. With an explicit ±one-frame schedule tolerance, the cut checklist would pass and there would be no unexplained >5 events. No such tolerance was specified, so the exact-timestamp exceptions are flagged here. This report does not claim these offsets were newly introduced in v7.

- **0≤t<1s:** maximum score **0.115 at 0.708333s**. No >5 discontinuity; former 0.333s frontal flash removed.
- **22<t<23s:** maximum score **0.116 at 22.375s**. No >5 discontinuity; former 22.25s plain-background head removed. The scheduled cut at exactly 22s scores 19.923 and is necessarily excluded from this clip-head test.
- All other >5 events are the scheduled transitions or their one-frame-late counterparts listed above. No other event requires a subtitle-boundary exemption to explain a score above 5.

## 3. Subtitles — PASS

All eleven SRT dialogue strings match the corresponding current SCRIPT.md dialogue cells word-for-word, including punctuation (speaker labels and offscreen directions excluded). Each SRT start equals its MP3's explicit `adelay` in the v7 build. ffprobe-measured MP3 durations give the expected ends below. Maximum absolute end error is **0.000476s**, well within **0.1s**. This is a text/placement check against the supplied script and recordings, not an independent speech transcription.

| MP3 | Build delay / SRT start (s) | MP3 duration (s) | Expected end (s) | SRT end (s) | Exact text match |
|---|---:|---:|---:|---:|---|
| f01 | 1.500 | 1.764717 | 3.264717 | 3.265 | PASS |
| d01 | 8.000 | 1.160998 | 9.160998 | 9.161 | PASS |
| f02 | 14.500 | 1.625397 | 16.125397 | 16.125 | PASS |
| d02 | 18.000 | 1.857596 | 19.857596 | 19.858 | PASS |
| f03 | 23.000 | 1.950476 | 24.950476 | 24.950 | PASS |
| r01 | 26.000 | 0.975238 | 26.975238 | 26.975 | PASS |
| d03 | 32.000 | 2.136236 | 34.136236 | 34.136 | PASS |
| d04 | 35.000 | 1.160998 | 36.160998 | 36.161 | PASS |
| d05 | 37.500 | 1.764717 | 39.264717 | 39.265 | PASS |
| f04 | 42.500 | 1.625397 | 44.125397 | 44.125 | PASS |
| d06 | 45.000 | 1.160998 | 46.160998 | 46.161 | PASS |

## 4. Voices — PASS

Estimated fundamental frequency from the final AAC-decoded audio, rather than merely the source MP3s: fourth-order 65–1000Hz bandpass, downsample to 16kHz, 64ms frames / 10ms hop, YIN-style cumulative normalized difference, 50–400Hz search, RMS floor 0.004 and periodicity threshold 0.2. Search bounds extend outside the acceptance range. These are pitch estimates, not speaker-identity verification; the fourth slot includes score.

| FIELDER slot (s) | Median pitch (Hz) | Accepted voiced frames | Required |
|---|---:|---:|---|
| 1.5–3.3 | 111.64 | 70 | 85–180Hz: PASS |
| 14.5–16.1 | 103.26 | 64 | 85–180Hz: PASS |
| 23–25 | 134.95 | 76 | 85–180Hz: PASS |
| 42.5–44.1 | 136.36 | 122 | 85–180Hz: PASS |

## 5. Music — PASS against current MUSIC_CUES.md and requested thresholds

Mean level is RMS dBFS of the final mono audio decoded to 48kHz floating-point samples, using exact start-inclusive/end-exclusive windows. All requested audible windows are free of scheduled speech.

| Window (s) | Mean dBFS | Criterion | Result |
|---|---:|---|---|
| 11-13 | -27.53 | > −35dBFS | PASS |
| 27.2-29.2 | -27.53 | > −35dBFS | PASS |
| 50-54 | -32.32 | > −35dBFS | PASS |
| 56-58.5 | -25.54 | > −35dBFS | PASS |
| 55-56 | -100.88 | < −80dBFS | PASS |

The audible motif, final swell and title note agree with the current MUSIC_CUES.md design and v7 build recipe. The black-gap mean passes; AAC boundary residue means decoded samples are not mathematically all zero.

**Remaining document conflict:** PACING_NOTES.md shot 08 says “digital silence” and its closing paragraph says “without musical relief”; SCRIPT.md also calls shots 07–08 “digitally silent.” MUSIC_CUES.md explicitly requires T1 at 56s. The film follows MUSIC_CUES.md, so the requested music check passes, but full compliance with all current documents is impossible. The title measures −25.54dBFS rather than silence. These silence statements still need reconciliation outside this review.

## 6. Requested frames — PASS

Inspected final-video frames at exactly the eight requested timestamps (native frame indices 12, 48, 456, 540, 624, 864, 1080 and 1392).

| Time | Observed evidence | Result |
|---:|---|---|
| 0.5s | Side-facing Fielder in domestic interior; no frontal take | PASS |
| 2s | Same side-facing Fielder take and setting as 0.5s; opening question subtitle | PASS |
| 19s | Dan: short neat dark hair, clean-shaven, olive rain jacket and gray sweater; gilt-framed Cubist portrait behind him | PASS |
| 22.5s | Roy in interview-room take, framed art and crutches visible | PASS |
| 26s | Same Roy take and room as 22.5s; no plain-background head; “Never. Not once.” subtitle | PASS |
| 36s | Fielder silent reaction close-up, mouth closed, under Dan's “Why would I deceive you?” | PASS: explicitly expected by reconciled shot-05 direction |
| 45s | Dan in matching tight close-up and rain jacket; eyes closed at this sampled instant, consistent with a blink | PASS |
| 58s | Black title card reads exactly **YOU CAN SEE ANYTHING** | PASS |

Dan and Roy's visible wardrobe/face details are consistent with the character bible; age, ethnicity and injury history cannot be established from appearance alone. The tight samples do not establish every set-dressing item or continuous lens contact/mouth closure throughout entire shots. The requested frame checks and scene scan establish the head fixes together, rather than extrapolating absence of flashes from two stills alone.
