# QC report — teaser v6

Reviewed 2026-10-18. Review only; no media, subtitle, dialogue, or build files changed. Sources: SCRIPT.md, PACING_NOTES.md, MUSIC_CUES.md, build/build_teaser_v6.sh, build/v6/teaser.srt, dialogue/v2/*.mp3, and ../dan-and-roy-parking/CHARACTER_BIBLE.md.

## 1. Technical — PASS

ffprobe reports container, video and audio durations of 60.000000 seconds; 1920×1080 H.264; nominal and average frame rates 24/1; 1,440 video frames. Audio is present: AAC, 48,000 Hz, mono. Note: MUSIC_CUES.md specifies stereo PCM; the delivered audio differs from that document even though it passes the requested technical checklist.

## 2. Subtitles — FAIL

Three of eleven SRT entries differ word-for-word from SCRIPT.md:

| Entry / start | SRT text | Required SCRIPT.md text |
|---|---|---|
| 1 / 1.500s | And the county approved the parking? | Removing the food bank was justified? |
| 3 / 14.500s | The building was a food bank. | Why did people lose access? |
| 5 / 23.000s | It says here the neighbors objected. | Ever wondered if Dan was misleading you? |

Entries 2, 4, 6–11 match SCRIPT.md exactly. This is a text comparison against the script, not an independent transcription of the recordings.

Timing passes for all eleven entries. MP3 durations measured with ffprobe; decoded sample counts independently agree within 0.00005s. Expected end = build-script delay + MP3 duration. Every start equals its build delay; every end differs by less than 0.001s, comfortably within 0.1s.

| Entry / MP3 | Delay / SRT start (s) | MP3 duration (s) | Expected end (s) | SRT end (s) |
|---|---:|---:|---:|---:|
| 1 / f01 | 1.500 | 1.764717 | 3.264717 | 3.265 |
| 2 / d01 | 8.000 | 1.160998 | 9.160998 | 9.161 |
| 3 / f02 | 14.500 | 1.625397 | 16.125397 | 16.125 |
| 4 / d02 | 18.000 | 1.857596 | 19.857596 | 19.858 |
| 5 / f03 | 23.000 | 1.950476 | 24.950476 | 24.950 |
| 6 / r01 | 26.000 | 0.975238 | 26.975238 | 26.975 |
| 7 / d03 | 32.000 | 2.136236 | 34.136236 | 34.136 |
| 8 / d04 | 35.000 | 1.160998 | 36.160998 | 36.161 |
| 9 / d05 | 37.500 | 1.764717 | 39.264717 | 39.265 |
| 10 / f04 | 42.500 | 1.625397 | 44.125397 | 44.125 |
| 11 / d06 | 45.000 | 1.160998 | 46.160998 | 46.161 |

## 3. Picture cuts — FAIL

Ran FFmpeg `scdet=threshold=0.4` on the final MP4 at its native resolution. This is scdet's 0–100 score scale. There were 74 above-threshold events. Intended cuts at 6, 14, 22, 30, 34, 40, 42 and 55s register; the title appearance at 56s scores 0.368, below threshold, but is present.

Two substantial unscheduled cuts were confirmed by inspecting adjacent frames:

- **0.333333s**, score **22.939**: frontal Fielder image changes abruptly to the side-facing take.
- **22.250000s**, score **15.585**: Roy against a plain background changes abruptly to the interview room with framed art and crutches.

The following are ALL 46 suspected glitch candidates (including the two confirmed cuts above) after excluding exact intended cut times and events within one 24fps frame (0.041667s) of an SRT on/off boundary. That allowance accounts for subtitle frame quantization; it does not exclude neighboring picture-cut frames. Small scores can reflect ordinary facial motion, so these are flags, not confirmed editing defects.

| Timestamp (s) | scdet score |
|---:|---:|
| 0.333333 | 22.939 |
| 2.625000 | 0.595 |
| 3.333333 | 0.582 |
| 5.708333 | 0.567 |
| 5.750000 | 0.425 |
| 5.958333 | 0.564 |
| 14.041667 | 0.797 |
| 14.083333 | 0.548 |
| 22.250000 | 15.585 |
| 25.000000 | 0.593 |
| 26.083333 | 0.473 |
| 26.375000 | 0.433 |
| 26.666667 | 0.535 |
| 28.625000 | 0.473 |
| 28.791667 | 0.482 |
| 34.666667 | 0.466 |
| 34.833333 | 0.525 |
| 34.916667 | 0.692 |
| 35.125000 | 0.458 |
| 35.166667 | 1.119 |
| 35.208333 | 1.131 |
| 35.250000 | 0.554 |
| 35.291667 | 1.140 |
| 35.375000 | 0.624 |
| 35.833333 | 0.690 |
| 36.041667 | 0.717 |
| 36.083333 | 0.765 |
| 36.666667 | 0.468 |
| 37.000000 | 0.729 |
| 37.041667 | 0.699 |
| 37.125000 | 0.580 |
| 37.291667 | 0.442 |
| 37.375000 | 0.594 |
| 37.583333 | 0.509 |
| 37.916667 | 0.417 |
| 37.958333 | 0.411 |
| 38.083333 | 0.476 |
| 38.125000 | 1.047 |
| 38.166667 | 0.716 |
| 38.208333 | 0.638 |
| 38.333333 | 0.459 |
| 38.583333 | 0.578 |
| 38.625000 | 0.561 |
| 38.708333 | 0.783 |
| 39.333333 | 0.477 |
| 40.041667 | 0.566 |

## 4. Voices — PASS

Estimated pitch from the final video's decoded audio using a YIN-style difference estimator, 64ms frames / 10ms hop, 65–1000Hz bandpass, 50–400Hz search, and energy/periodicity rejection of unvoiced frames. Search bounds deliberately extend outside the acceptance range. These are signal estimates, not speaker-identity verification; the last slot includes underlying score.

| FIELDER slot (s) | Median pitch (Hz) | Accepted voiced frames | Required median |
|---|---:|---:|---|
| 1.5–3.3 | 110.8 | 92 | 85–180Hz |
| 14.5–16.1 | 96.5 | 85 | 85–180Hz |
| 23–25 | 131.9 | 99 | 85–180Hz |
| 42.5–44.1 | 131.7 | 140 | 85–180Hz |

No slot's median is outside the requested range.

## 5. Music — PASS (requested level thresholds)

Measured RMS mean dBFS on native 48kHz float-decoded final audio, with exact start-inclusive/end-exclusive windows. A speech-free room-tone comparison at 5–6s measures −61.56dBFS.

| Window (s) | Mean dBFS | Criterion | Result |
|---|---:|---|---|
| 11–13 | −27.53 | > −35 | Meets |
| 27.2–29.2 | −27.53 | > −35 | Meets |
| 50–54 | −32.32 | > −35 | Meets |
| 56–58.5 | −25.54 | > −35 | Meets |
| 55–56 | −100.88 | < −80 | Meets |

Music windows exceed the room-tone comparison by about 29–36dB. The black-gap mean passes; AAC boundary residue means this is not strictly zero samples.

**Source conflict:** these requested music checks and the v6 recipe disagree with MUSIC_CUES.md and PACING_NOTES.md. Those documents prohibit a swell, require no score in shot 06, and require digital silence throughout 55–60s. The measured 50–54s score and 56–58.5s title note violate those document requirements. MUSIC_CUES.md also specifies a much quieter 174.61Hz note at 11s, while the v6 recipe uses a louder 220Hz motif and adds a 27.2s note, sustained shot-06 score, and title note. Thus the level checklist passes, but document compliance does not.

## 6. Canon frames — FAIL

Inspected extracted frames at exactly 2, 19, 26, 36, 45 and 58s.

- **2s and 36s:** Fielder's dark wavy hair, facial structure and freckles are visually consistent. However, **36s shows Fielder during Dan's “Why would I deceive you?” line**. SCRIPT.md/PACING_NOTES.md assign shot 05 to Dan; this is a character/shot mismatch. The person at 36s visibly differs from Dan at 19s and 45s.
- **19s:** Dan has short neat dark hair, a clean-shaven face, an olive rain jacket and gray sweater. A gilt-framed Cubist portrait hangs behind him, consistent with the imitation Picasso requirement. Exact age cannot be established from a frame.
- **26s:** Roy has a lean face, short black hair, light stubble, dark hoodie fabric at the shoulders, visible crutches on the right, and gilt-framed Cubist art behind him. The close crop limits assessment of his full build and hoodie wear. Filipino-American identity and the skiing origin of a knee injury cannot be verified from appearance; there is no visible contradiction of those story details.
- **45s:** Dan returns, wearing the rain jacket; visually consistent with 19s and inconsistent with the person shown at 36s.
- **58s:** Black title card reads exactly **YOU CAN SEE ANYTHING**.

The silver laptop with red Pinterest logo is not visible in these tightly cropped samples, so that set-dressing detail is unverified, not established absent from the entire video.

## Overall verdict — FAIL

Technical delivery, subtitle timing, estimated voice medians, and the requested music levels pass. Three subtitle texts conflict with the script; two unscheduled picture cuts are confirmed, with additional low-threshold candidates listed; and Fielder appears during Dan's shot-05 dialogue. Music also conflicts with the project's written silence/score requirements. No fixes were made.
