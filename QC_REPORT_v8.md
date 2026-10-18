# QC REPORT — v8 breakdown cut

Reviewed 2026-10-18. **Overall verdict: FAIL.** Review only; no media, source, subtitle, score, or build files changed.

| Check | Result | Finding |
|---|---|---|
| 1. Technical | PASS | Exactly 60.000000s, 1920×1080, 24/1 fps, 1,440 decoded video frames; AAC audio present. |
| 2. Intertitle wording / sampled hard cuts | PASS | All eight midpoint transcriptions match word-for-word; cards 1 and 7 enter and leave on hard cuts. |
| 3. Collage / inserts | FAIL | Roy's required crutches and thin body silhouette are excluded by the crop. Dan's dominant panel changes to Fielder prematurely at 34.041667s. At requested 49s/51s, cards correctly override the grids under the plan. |
| 4. Subtitles | PASS | v8 and v7 SRT are byte-identical; all eleven dialogue texts match SCRIPT.md; no praise text. |
| 5. Picture edits | FAIL | Unexpected event at 34.041667s, score 13.075. No above-5 events inside the four insert windows. |
| 6. Audio | PASS (measured criteria) | Both mixes rise across the requested windows; exact PCM zero gap; title onset 56.002021s; all four Fielder pitch medians in range. Speech exceeds score in both dialogue samples, with limited separation in the second. Subjective audibility is not certified by these measurements. |
| 7. Score provenance | PASS | Existing PDF present; fresh LilyPond compile succeeds; section timings reconcile to 0/14/30/42/55/56s. |

## 1. Technical evidence

ffprobe with `-count_frames -show_streams -show_format`: container, video, and audio duration each 60.000000s; H.264, yuv420p, width 1920, height 1080; average and nominal rate both 24/1; `nb_frames=nb_read_frames=1440`. AAC LC, mono, 48,000 Hz. PCM master: 48,000 Hz, signed 16-bit mono, exactly 2,880,000 samples. Raw AAC decoding produces 512 extra padding samples; stream/container duration remains exactly 60 seconds.

## 2. Cards: extracted frames and exact readings

Read directly from extracted final-video frames, with line breaks normalized to spaces:

| Card | Midpoint (s) | Exact visible text | Result |
|---|---:|---|---|
| 1 | 5.125 | A NEW DOCUMENTARY BY NATHAN FIELDER | PASS |
| 2 | 21.125 | AN EXTRAORDINARY ACT OF LISTENING | PASS |
| 3 | 31.125 | A BRAVE NEW LANGUAGE OF TRUTH | PASS |
| 4 | 40.875 | CINEMA WILL NEVER BE THE SAME | PASS |
| 5 | 48.875 | BEYOND TRUTH. BEYOND CINEMA. | PASS |
| 6 | 51.125 | A WORK OF IMPOSSIBLE GENIUS | PASS |
| 7 | 53.000 | A POSTMODERN MASTERPIECE | PASS |
| 8 | 54.500 | THE GREATEST FILM YOU WILL EVER SEE IN YOUR LIFE | PASS |

Card 8 uses four lines: `THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE`.

Hard-cut comparisons (last preceding frame vs first following frame):

- Card 1 entry: frame 107 at 4.458333s is Fielder; frame 108 at 4.500000s is the complete card. Exit: frame 137 at 5.708333s is the complete card; frame 138 at 5.750000s is Fielder.
- Card 7 entry: frame 1259 at 52.458333s is the complete 3×3 grid; frame 1260 at 52.500000s is the complete card. Exit: frame 1283 at 53.458333s is the complete card; frame 1284 at 53.500000s is the complete mixed 4×4 grid.

No blended picture/text or partial-opacity transition appears in those adjacent-frame comparisons. Cards are centered, pale white on black; build script specifies `0xF5F2EA`, rather than literal RGB white.

## 3. Requested picture samples

| Requested time | Observation | Result |
|---:|---|---|
| 6.7s | Full-frame wet parking lot, lone light-colored sedan, rain and reflections. | PASS |
| 11s | Full-frame empty rainy lot with fresh bright painted parking lines. | PASS |
| 16s | Full-frame food-bank exterior, FOOD BANK sign, people queued outside; dialogue subtitle in global lane. | PASS |
| 25s | Two panels: extreme Fielder reaction crop left, Roy face/neck right. Crop excludes crutches and nearly all clothing/body; thin silhouette and hoodie cannot be established. | FAIL |
| 28.5s | Demolition/excavator and falling material left; Roy close-up right. Same canon visibility problem persists. | FAIL for Roy visibility; panel assignment PASS |
| 33s | Dan fills left two-thirds, extreme Fielder crop right third; first-sentence subtitle intact. | PASS at sample; later premature switch FAIL |
| 37s | Food bank left quarter, mouth-closed Fielder reaction central half, empty lot right quarter; no speaking Dan visible. | PASS |
| 44s | Dan stare split vertically; small visible discontinuity through nose/lips at center seam. Script confirms 8px right-panel vertical crop displacement followed by scaling. | PASS |
| 49s | Card 5: BEYOND TRUTH. BEYOND CINEMA. | PASS against plan; requested four-panel image is masked here |
| 51s | Card 6: A WORK OF IMPOSSIBLE GENIUS. | PASS against plan; requested nine-panel image is masked here |
| 53.7s | 4×4 grid: fourteen Dan cells, empty lot at row 2/column 2 and demolition at row 3/column 3. | PASS |
| 57s | Static centered YOU CAN SEE ANYTHING on black, no other words. | PASS |

Supplementary extracted samples at 49.85s and 51.9s confirm the uncovered 2×2 and 3×3 Dan grids respectively. The plan gives cards priority, so the absence of grids at exactly 49 and 51 seconds is not an edit failure.

The unexpected cut is visible between frame 816 (34.000000s: dominant Dan left) and frame 817 (34.041667s: dominant Fielder left); right-side Fielder remains. Dan is therefore absent for the final 0.094333s of the exact 32.000–34.136 subtitle interval and the final 0.458333s before the planned 34.500 picture boundary. The build script takes this entire segment from `build/v7/video_raw.mp4`, which retains the old reaction change; the segment boundary alone does not guarantee the intended hold.

## 4. Subtitles

Both SRT files are 705 bytes, SHA-256:

`5b2c8806b9eadd6363f3d7a9140fac2ab18a1351ba9b4d8434da782d6f59db06`

All eleven texts match the SCRIPT.md dialogue column, and all eleven start/end pairs match EDIT_PLAN.md's exact SRT table. SCRIPT.md's broader delivery slots are not mistaken for subtitle endpoints. No praise card text appears in the SRT. Extracted dialogue-bearing picture samples show a single global subtitle lane.

## 5. Scene-change scan

Command: `ffmpeg -i you-can-see-anything-teaser-v8.mp4 -vf 'scdet=threshold=0.4,metadata=print:file=/tmp/qcv8/scdet.txt' -an -f null -`.

Compared every `lavfi.scd.score > 5` against the union of planned card, shot, insert, panel, black, and title boundaries, with ±1 frame (0.041667s) tolerance. Allowed boundary set in seconds:

`0, 4.5, 5.75, 6, 7.5, 10, 12.5, 14, 14.5, 17.5, 20.5, 21.75, 22, 27.25, 29.75, 30, 30.5, 31.75, 34.5, 40, 41.75, 42, 47, 48, 49.75, 50, 50.5, 51.75, 52.5, 53.5, 54, 55, 56, 60`.

**FAIL: 34.041667s / frame 817 / score 13.075** is outside that tolerance. It is 11 frames before 34.500s. The event at 30.041667s (9.514) is within the explicitly allowed one-frame tolerance of 30s, although it indicates an adjacent-frame source change worth distinguishing from the planned composition boundary.

All above-5 events:

| Time (s) | scdet score | Boundary match |
|---:|---:|---|
| 4.500000 | 27.845 | PASS |
| 5.750000 | 28.328 | PASS |
| 6.000000 | 26.399 | PASS |
| 7.500000 | 24.283 | PASS |
| 10.000000 | 23.059 | PASS |
| 12.500000 | 21.689 | PASS |
| 14.000000 | 15.241 | PASS |
| 14.500000 | 17.592 | PASS |
| 17.500000 | 17.640 | PASS |
| 20.500000 | 31.776 | PASS |
| 21.750000 | 32.920 | PASS |
| 22.000000 | 19.443 | PASS |
| 27.250000 | 9.596 | PASS |
| 29.750000 | 9.116 | PASS |
| 30.000000 | 19.387 | PASS |
| 30.041667 | 9.514 | PASS |
| 30.500000 | 27.193 | PASS |
| 31.750000 | 27.379 | PASS |
| 34.041667 | 13.075 | **FAIL** |
| 34.500000 | 20.895 | PASS |
| 40.000000 | 33.012 | PASS |
| 41.750000 | 35.128 | PASS |
| 42.000000 | 10.408 | PASS |
| 47.000000 | 19.001 | PASS |
| 48.000000 | 30.090 | PASS |
| 49.750000 | 31.653 | PASS |
| 50.000000 | 17.054 | PASS |
| 50.500000 | 30.876 | PASS |
| 51.750000 | 31.259 | PASS |
| 52.500000 | 31.186 | PASS |
| 53.500000 | 33.068 | PASS |
| 54.000000 | 32.604 | PASS |
| 55.000000 | 33.768 | PASS |

No >5 event occurs strictly inside sedan 6–7.5s, lot 10–12.5s, food bank 14.5–17.5s, or demolition 27.25–29.75s; none occurs in their later visible collage reuse either. Build-script source trims are sedan 1–2.5s, lot 2–4.5s, food bank 1–4s, demolition 3–5.5s. This verifies the final at the requested detector cutoff; it does not assert absence of subtler discontinuities below that cutoff.

## 6. Audio measurements

“Mean level” below means whole-window RMS expressed as dBFS, `20 log10(sqrt(mean(samples²)))`, including pauses. AAC is decoded to floating-point PCM; PCM measurements use the supplied master.

| Window | Final AAC dBFS | PCM master dBFS |
|---|---:|---:|
| 0–10s | -27.817 | -27.810 |
| 20–28s | -25.585 | -25.575 |
| 32–40s | -23.449 | -23.440 |
| 42–48s | -20.221 | -20.214 |
| 50–54s | -13.854 | -13.847 |

**PASS:** every successive window rises in both versions.

**PASS — digital silence:** native PCM samples 2,640,000–2,687,999 are all exactly integer zero (0/48,000 nonzero). AAC contains 384 nonzero decoded samples within 55–56s, peak 0.001995919 (approximately −54.0 dBFS), consistent with codec boundary residue. The plan explicitly designates PCM as the exact-silence reference; the AAC is not digitally zero.

**PASS — title onset:** first absolute master sample above −50 dBFS at/after 56s is sample 2,688,097, time **56.002020833s**, +2.021ms from target, within ±10ms.

Dialogue-window measurements use supplied dialogue and score stems as supporting evidence (stem separation is not inferred from mixed RMS):

| Window | Final AAC | PCM mix | Dialogue stem | Score stem | Dialogue minus score |
|---|---:|---:|---:|---:|---:|
| 1.6–3.0s | -23.278 | -23.269 | -23.269 | -inf | score silent |
| 45–46.1s | -20.902 | -20.895 | -22.779 | -25.457 | +2.678 dB |

**PASS by measured energy dominance:** opening dialogue has no score energy; final answer exceeds score by 2.678 dB. The second window has modest separation and should not be described as comfortably ducked solely from its RMS. No calibrated speaker/headphone listening assessment was performed; audible masking/ducking remains a subjective review limitation.

**PASS — Fielder pitch:** broad-range autocorrelation estimator (search approximately 60–350 Hz, 50ms frames, 10ms hop, correlation >0.55, level gate; 65–900 Hz prefilter). Acceptance range was not imposed on the estimator. Medians are voiced-frame estimates, not averages over silence.

| Slot | Final AAC median Hz | PCM median Hz | Dialogue-stem median Hz |
|---|---:|---:|---:|
| 1.5–3.3s | 110.34 | 110.34 | 110.34 |
| 14.5–16.1s | 94.12 | 94.12 | 91.43 |
| 23–25s | 150.94 | 150.94 | 127.49 |
| 42.5–44.1s | 158.42 | 158.42 | 151.66 |

All medians are within 85–180 Hz; dialogue-stem cross-check reduces music-related pitch ambiguity.

## 7. Score provenance and timing

`score/score.pdf` exists (143,891 bytes). Fresh compilation used `lilypond -o /tmp/qcv8/score score/score.ly`, exited 0, generated PDF and MIDI, and ended “Success: compilation successfully completed”; no bar-duration warnings. Existing PDF was rasterized and inspected, and its text extracted: all six section markings are present. Late markings are crowded in the engraving but retain their intended musical locations.

At quarter=60 with no tempo changes:

| Start | Section | Bar arithmetic |
|---:|---|---|
| 0s | almost nothing | Bars 1–3: 12 quarters; bar 4: 2; total 14 |
| 14s | small wrongness | Bars 5–8: 16 quarters; cumulative 30 |
| 30s | the assurance fractures | Bars 9–11: 12 quarters; cumulative 42 |
| 42s | beauty curdles | Bars 12–14: 12 quarters; bar 15: 1; cumulative 55 |
| 55s | DIGITAL SILENCE | Bar 16: 1 quarter rest on every part; cumulative 56 |
| 56s | title / decay to 1:00 | Bar 17: 4 quarters, one chord per part; cumulative 60 |

All four parts account for the same 60 quarter notes, including metered tuplets. These timings match the .ly markings and rendered notation. This establishes score compilation and section timing, not a sample-for-sample proof that the supplied score stem was synthesized from that MIDI.

## Review artifacts and scope

Temporary extracted PNG frames, contact sheets (`cards.jpg`, `samples.jpg`, `edges.jpg`), `scdet.txt`, `events.json`, audio measurement JSON, fresh score PDF/MIDI and compile log are in `/tmp/qcv8/` for this session. They are review scratch artifacts; only this report was added to the project. The build script was read, not executed. Its scope is picture assembly; it does not itself produce the final subtitle/audio mux. No fixes were made.
