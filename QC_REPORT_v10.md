# QC_REPORT_v10

Date: 2026-10-18. Verification only; no production assets changed.

**Overall verdict: FAIL against the complete build spec.** The headline minimum-duration audit **PASSES**: all 27 rendered segments match the planned boundaries; minimum **2.000s / 48 frames**. Technical, card wording/overlap, requested picture samples, subtitle identity, score compilation/provenance, pitch, escalation, title timing and stem separation pass. Failure: the saved score stem contains substantial audio during the mandated all-bus 65–67s silence. Additional build-spec picture failure: the Tesla touchscreen has a blue/purple background rather than the specified black display; the windshield also contains faint exterior detail before the reveal rather than pure black.

Audited artifact: `you-can-see-anything-teaser-v10.mp4` (32,888,130 bytes).
SHA-256: `3a113d809c6bb4d631c6476f8419f82952d1b5153fc9f1b5e0fc1e4981a20c5f`.

Read order: RULES.md first, then EDIT_PLAN_V10.md, score/score10.ly and SCRIPT.md. RULES.md takes precedence; dialogue timing follows the locked SRT rather than the older delivery slots in SCRIPT.md.

## 1. RULES AUDIT — PASS

| Rule | Result | Evidence |
|---|---|---|
| 1: Every picture segment ≥2.000s | PASS | Exhaustive rendered-boundary audit below; minimum 48 frames. No extra cut detected beyond the planned boundaries. |
| 2: Longer beats extend the film | PASS for specified timeline | Render retains the prescribed S01–S26 boundaries through 71s and adds S27 through 76s; black remains 2s and title 4s. No borrowing from another specified hold. Historical editing intent cannot be inferred from the render alone. |
| 3: Dialogue/subtitles locked; no cards over speech | PASS for requested lock/overlap checks | SRT byte-identical to v7; all eight card windows disjoint from all eleven SRT intervals. Dialogue remains in those rendered windows. |
| 4: QC with full duration audit | PASS | This report includes all 27 segments and minimum. |
| 5: Verify rendered artifact | PASS | Final MP4 decoded/frame-counted, scene-scanned and visually sampled; encoded audio measured as well as PCM/stems. Score source checks are separately identified. |

### Full rendered duration audit

Frame indices are zero-based, start-inclusive/end-exclusive. Boundaries were checked with adjacent rendered frame grabs and a full-file FFmpeg `scale=480:270,scdet=threshold=8` scan. A detector score is supporting evidence, not the definition of a cut. Low-contrast black/title transitions were confirmed by frame grabs. S27 starts black at frame 1704 and fades into the cabin (visible at 71.5s, fully established by 73s).

| Segment | Planned window (s) | Planned duration (s) | Rendered frames | Verified duration (s) | Start-boundary evidence | ≥2.000s |
|---|---:|---:|---:|---:|---|---|
| S01 | 0.000–4.000 | 4.000 | 0–96 | 4.000 | Opening frame inspected | PASS |
| S02 | 4.000–6.000 | 2.000 | 96–144 | 2.000 | Adjacent grabs; scdet 27.555 | PASS |
| S03 | 6.000–8.000 | 2.000 | 144–192 | 2.000 | Adjacent grabs; scdet 38.937 | PASS |
| S04 | 8.000–10.000 | 2.000 | 192–240 | 2.000 | Adjacent grabs; scdet 24.202 | PASS |
| S05 | 10.000–12.500 | 2.500 | 240–300 | 2.500 | Adjacent grabs; scdet 23.089 | PASS |
| S06 | 12.500–14.500 | 2.000 | 300–348 | 2.000 | Adjacent grabs; scdet 13.896 | PASS |
| S07 | 14.500–17.000 | 2.500 | 348–408 | 2.500 | Adjacent grabs; scdet 16.896 | PASS |
| S08 | 17.000–20.000 | 3.000 | 408–480 | 3.000 | Adjacent grabs; scdet 17.115 | PASS |
| S09 | 20.000–22.000 | 2.000 | 480–528 | 2.000 | Adjacent grabs; scdet 32.004 | PASS |
| S10 | 22.000–27.000 | 5.000 | 528–648 | 5.000 | Adjacent grabs; scdet 23.530 | PASS |
| S11 | 27.000–30.000 | 3.000 | 648–720 | 3.000 | Adjacent grabs; scdet 9.148 | PASS |
| S12 | 30.000–32.000 | 2.000 | 720–768 | 2.000 | Adjacent grabs; scdet 28.924 | PASS |
| S13 | 32.000–34.500 | 2.500 | 768–828 | 2.500 | Adjacent grabs; scdet 29.139 | PASS |
| S14 | 34.500–39.500 | 5.000 | 828–948 | 5.000 | Adjacent grabs; scdet 17.109 | PASS |
| S15 | 39.500–42.000 | 2.500 | 948–1008 | 2.500 | Adjacent grabs; scdet 31.705 | PASS |
| S16 | 42.000–47.000 | 5.000 | 1008–1128 | 5.000 | Adjacent grabs; scdet 32.438 | PASS |
| S17 | 47.000–49.000 | 2.000 | 1128–1176 | 2.000 | Adjacent grabs; scdet 19.192 | PASS |
| S18 | 49.000–51.000 | 2.000 | 1176–1224 | 2.000 | Adjacent grabs; scdet 31.141 | PASS |
| S19 | 51.000–54.000 | 3.000 | 1224–1296 | 3.000 | Adjacent grabs; scdet 31.126 | PASS |
| S20 | 54.000–56.000 | 2.000 | 1296–1344 | 2.000 | Adjacent grabs; scdet 30.842 | PASS |
| S21 | 56.000–58.500 | 2.500 | 1344–1404 | 2.500 | Adjacent grabs; scdet 32.522 | PASS |
| S22 | 58.500–60.500 | 2.000 | 1404–1452 | 2.000 | Adjacent grabs; scdet 32.613 | PASS |
| S23 | 60.500–62.500 | 2.000 | 1452–1500 | 2.000 | Adjacent grabs; scdet 32.397 | PASS |
| S24 | 62.500–65.000 | 2.500 | 1500–1560 | 2.500 | Adjacent grabs; scdet 32.155 | PASS |
| S25 | 65.000–67.000 | 2.000 | 1560–1608 | 2.000 | Adjacent grabs (card → black) | PASS |
| S26 | 67.000–71.000 | 4.000 | 1608–1704 | 4.000 | Adjacent grabs (black → title) | PASS |
| S27 | 71.000–76.000 | 5.000 | 1704–1824 | 5.000 | Adjacent grabs (title → black/cabin fade) | PASS |

**Minimum found: 2.000s / 48 frames. Total: 76.000s / 1,824 frames.** Card 8 is 2.500s, black is 2.000s, title is 4.000s. Terminal boundary is EOF at frame 1824, 76.000s.

**S27 adjudication: PASS, continuous composition.** The only additional scdet event is 74.458333s, score 13.807. For 74.42s, inspected the actual display frame containing that instant: frame 1786 at 74.416667s. Compared with frame 1788 at 74.500000s. Steering wheel, dash, screen, windshield framing and viewpoint continue; exterior illumination changes dramatically and reveals the food bank. This is the specified headlight change within S27, not a new picture segment. S27 remains 5.000s. A time-seek grabbing the next frame at 74.458333s would misleadingly show the already illuminated view for a nominal 74.42s request; frame-index extraction avoids that error. The earlier windshield is very dark, with faint building/ground detail, rather than mathematically pure black.

## 2. Technical — PASS

FFprobe with decoded-frame counting reports H.264, 1920×1080, progressive, `r_frame_rate=24/1`, `avg_frame_rate=24/1`, 1,824 stored and decoded video frames, video duration 76.000000s and container duration 76.000000s. AAC mono audio is present at 48,000Hz with stream duration 76.000000s. PCM mix is mono signed 16-bit, 48,000Hz, exactly 3,648,000 samples (76.000s); dialogue stem is the same length/format and score stem is stereo at the same rate/length.

## 3. Cards — PASS

Exact visual transcriptions from the rendered midpoints follow. All match plan wording and punctuation. Card 8 line breaks are shown with `/` separators, not literal slashes on screen.

| Card | Rendered window (s) | Midpoint (s) | Exact text | Text match | Speech intersection |
|---|---:|---:|---|---|---|
| 1 | 4.000–6.000 | 5.000 | A NEW DOCUMENTARY BY NATHAN FIELDER | PASS | None — PASS |
| 2 | 20.000–22.000 | 21.000 | AN EXTRAORDINARY ACT OF LISTENING | PASS | None — PASS |
| 3 | 30.000–32.000 | 31.000 | A BRAVE NEW LANGUAGE OF TRUTH | PASS | None — PASS |
| 4 | 39.500–42.000 | 40.750 | CINEMA WILL NEVER BE THE SAME | PASS | None — PASS |
| 5 | 49.000–51.000 | 50.000 | BEYOND TRUTH. BEYOND CINEMA. | PASS | None — PASS |
| 6 | 54.000–56.000 | 55.000 | A WORK OF IMPOSSIBLE GENIUS | PASS | None — PASS |
| 7 | 58.500–60.500 | 59.500 | A POSTMODERN MASTERPIECE | PASS | None — PASS |
| 8 | 62.500–65.000 | 63.750 | THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE | PASS | None — PASS |

Intersection test used start-inclusive/end-exclusive intervals against all 11 windows in `build/v10/teaser.srt`: overlap iff `card_start < speech_end and speech_start < card_end`. Zero intersections among all 88 pairs. Clear-film gaps are 14.000, 8.000, 7.500, 7.000, 3.000, 2.500 and 2.000s, strictly decreasing.

## 4. Requested picture samples — PASS; additional S27 styling check — FAIL

| Time | Rendered observation | Result |
|---:|---|---|
| 7.000 | Full-frame white sedan in wet, rainy parking lot. | PASS |
| 15.500 | Food-bank frontage, queue and supplies; subtitle “The building was a food bank.” | PASS |
| 25.000 | Two panels: Fielder reaction left, Roy face right. Roy's face and the paired metal crutches with dark underarm pads are visible at the right edge; crutches are partially cropped but recognizable. Right panel has blurred padding above/below the sharp image strip. | PASS |
| 28.500 | Excavator demolishing building left; Roy and visible crutches right. | PASS |
| 33.000 | Dan occupies dominant left two-thirds with speaking-line subtitle; Fielder reaction occupies narrower right panel. Adjacent boundary samples also show Dan's mouth changing through the line. | PASS |
| 37.000 | Food bank left, closed-mouth Fielder reaction center, empty lot right. No Dan image. | PASS |
| 44.000 | Dan split stare; subtle vertical discontinuity at the central seam; Fielder question subtitle. | PASS |
| 48.000 | Four Dan tiles in 2×2 geometry with crop offsets. | PASS |
| 52.500 | Nine Dan tiles in 3×3 geometry; recognizable central face/lens contact. | PASS |
| 57.000 | 4×4 grid, empty lot at zero-based cell 5 and demolition at cell 10. | PASS |
| 68.500 | Centered title “YOU CAN SEE EVERYTHING” on black. First title frame also verified at 1608 / 67.000s. | PASS |
| 73.000 | Dark Tesla cabin, steering wheel left, center touchscreen reading “YOU CAN SEE EVERYTHING.” | PASS for requested sample |
| 75.500 | Same cabin/viewpoint and title screen; food bank clearly illuminated through windshield. | PASS |

Additional plan compliance: **FAIL** — S27 calls for white text on the touchscreen's black display and pure black outside before the reveal. The rendered touchscreen has prominent blue/purple gradients and UI icons; faint exterior building/ground detail is visible before illumination. This does not constitute a cut or invalidate the duration audit. The requested dark-cabin/title/reveal composition itself is present.

## 5. Subtitles — PASS

`build/v10/teaser.srt` and `build/v7/teaser.srt` are byte-identical (705 bytes each).
Both SHA-256: `5b2c8806b9eadd6363f3d7a9140fac2ab18a1351ba9b4d8434da782d6f59db06`.

## 6. Audio — FAIL overall (all-bus silence)

Measurements use linear PCM normalized to full scale. Levels below are RMS dBFS unless explicitly labeled peak. Encoded values are measured after decoding the MP4 AAC track. No loudness normalization applied.

| Check | Measurement | Result |
|---|---|---|
| Mix samples 3,120,000–3,215,999 inclusive exactly zero | All 96,000 samples equal zero. | PASS |
| Dialogue stem same zero interval | All 96,000 samples equal zero. | PASS |
| Score stem same zero interval / gate every bus | 134,481 nonzero channel samples out of 192,000; peak 0.376251 full scale, RMS −32.138dBFS. Saved stem is not gated. | **FAIL** |
| Title onset relative to 67.000, first sample above −50dBFS | Mix +0.002021s (absolute 67.002021); encoded +0.001938s; score stem +0.001875s. All within ±0.010s. | PASS |
| Mean-level escalation | See table below; all successive required windows rise. | PASS |
| Maintain climax 62.5–65 | Mix −13.208dBFS versus −13.518 over 48–62.5; score −14.707 versus −14.958. No collapse before silence. | PASS |
| Dialogue/score separation, 45–46.161 | Dialogue −23.013; score stereo RMS −30.061; difference +7.048dB. Mono-averaged score −32.159, giving +9.146dB. Both exceed 5dB. | PASS |
| Near-silence 75–76 | Mix RMS −71.412; encoded −71.421; score −73.303; dialogue exact zero. | PASS on RMS level |
| Fielder medians in four exact SRT slots | All within 85–180Hz, including final encoded audio; table below. | PASS |

The 75–76s mix peak is −58.488dBFS (encoded −58.400); score peak −61.061. Thus “below −60dB” passes as an interval RMS/near-silence requirement, but **fails if intended as an every-sample peak ceiling for the mix**. Both measurements are disclosed rather than conflated.

AAC does not preserve exact digital zeros at the silent interval edges: 1,216 decoded samples are nonzero, maximum absolute amplitude 0.000396422 (about −68.04dBFS). The explicit exact-zero PCM mix test passes; encoded silence is near-silent, not bit-zero. The score-stem failure above is much larger and independent of AAC effects.

| Window (s) | PCM mix RMS dBFS | Score stereo RMS dBFS | Encoded mix RMS dBFS |
|---|---:|---:|---:|
| 0–10 | −27.810 | −47.853 | −27.817 |
| 20–28 | −25.575 | −29.759 | −25.585 |
| 32–40 | −23.440 | −27.048 | −23.449 |
| 42–48 | −20.783 | −23.086 | −20.790 |
| 48–62.5 reference climax | −13.518 | −14.958 | −13.525 |
| 62.5–65 | −13.208 | −14.707 | −13.214 |

Pitch method: normalized autocorrelation on 40ms windows every 10ms, search 60–300Hz (not restricted to the passing range), reject RMS below −45dBFS and correlation below 0.55, median of retained voiced frames. Measured both isolated dialogue and final encoded mix; music can alter mixed-track estimates, so both are reported.

| Fielder SRT window (s) | Dialogue median Hz (voiced frames) | Encoded median Hz (voiced frames) | Result |
|---|---:|---:|---|
| 1.500–3.265 | 111.89 (69) | 111.89 (69) | PASS |
| 14.500–16.125 | 107.38 (57) | 108.23 (66) | PASS |
| 23.000–24.950 | 135.59 (69) | 162.16 (73) | PASS |
| 42.500–44.125 | 158.42 (103) | 157.38 (79) | PASS |

## 7. Score provenance — PASS

Ran `python3 score/verify_score10.py` successfully. LilyPond compiled `score/score10.ly` to disposable PDF and MIDI under `/tmp`, exit 0, no warnings. LilyPond's evaluated lengths are 76.000 quarter notes each for pianoRH, pianoLH, strings and brass; global also totals 76.000. Quarter=60 makes each quarter one second. All A–C notation tokens match `score/score.ly` after removing comments and normalizing whitespace, for every part and global (stronger than note-only identity). The verifier additionally passes its frozen A–E hashes and confirms each title part is one attack tied for 4+4+1 quarters.

## Delivery verdict

**FAIL full-spec QC; PASS headline duration rule.** No segment shorter than 2.000s was found. Required unresolved failures are the score stem's 65–67s nonzero audio and S27's display/exterior styling differences. Final mix is correctly gated in PCM; all other requested measurements pass with the stated RMS-versus-peak qualification. This report makes no claim of a complete perceptual lip-sync or listening review beyond the requested frame/pitch/level measurements. No fixes applied.


## Re-QC — 2026-10-18

Focused verification after fixes; read RULES.md and EDIT_PLAN_V10.md, including S27 and sound requirements. Only this report was modified. Earlier findings remain historical; this section supersedes their verdict for the rechecked items. No broader QC rerun is claimed.

Artifact: `you-can-see-anything-teaser-v10.mp4`, 32,243,947 bytes. SHA-256: `c97107316b85f1e893b58073a129c2f13091a69366cb12dc33365b89e12d077b`.

### Audio — PASS

PCM measurements use signed 16-bit samples normalized by 32768; onset is the first sample above −50 dBFS after 67s, consistent with the original report.

| Recheck | Evidence | Result |
|---|---|---|
| Score-stem 65–67s exact zeros, both channels | 48 kHz stereo; samples 3,120,000–3,215,999 inclusive: zero nonzero samples in each channel (0/192,000 channel samples); peak exactly 0. | PASS |
| Mix 65–67s exact zeros | Same inclusive interval: all 96,000 mono samples exactly zero. | PASS |
| Mix length | Exactly 3,648,000 samples at 48 kHz (76.000s); score stem also 3,648,000 frames per channel. | PASS |
| Title onset 67.000 ±0.010s | Mix 67.002021s; score 67.001875s. | PASS |
| Overall mix peak near −0.31 dBFS | −0.305642 dBFS. | PASS |
| Mix 75–76s RMS below −60 dBFS | −71.411856 dBFS; score −73.302555 dBFS. | PASS |

The prior score-stem silence failure is resolved.

### Coda styling — FAIL (exterior only)

Decoded the rendered MP4 sequentially and selected zero-based frame indices with FFmpeg `select`, without time-seeking. Inspected full-resolution frames 1728 (72s), 1752 (73s), 1776 (74s), 1800 (75s), and 1812 (75.5s), plus frames 1786–1788 around the reveal. Reviewed a contact sheet containing every S27 frame (1704–1823) for continuity.

| Recheck | Observation | Result |
|---|---|---|
| Black touchscreen with only white YOU CAN SEE EVERYTHING | All five requested samples show the exact title, wrapped as YOU CAN SEE / EVERYTHING, on a black display. No gradient or UI icons on the display; blue cabin trim is outside it. | PASS |
| Exterior effectively black before switch | Very dark, but faint exterior/building detail and a blue light remain discernible at 72–74s. Frame 1786 (74.416667s), still before the main switch, shows recognizable frontage and illuminated ground patches. The plan's pure-black exterior requirement is not fully met. | FAIL |
| Post-switch food-bank reveal, same composition | Frames 1800 and 1812 clearly show the illuminated food bank with the same cabin, touchscreen, and viewpoint. Main illumination change occurs at frame 1787 (74.458333s); frame 1788 (74.500000s) remains lit. | PASS |

The previous touchscreen styling failure is resolved; the exterior-black portion remains unresolved.

### Regression spot-check — PASS

| Recheck | Evidence | Result |
|---|---|---|
| Total runtime/frame count | FFprobe decoded-frame count: 1,824 frames at 24/1 fps; video and container duration both 76.000000s. | PASS |
| S27 remains one 71–76s segment | Frame 1703 retains the preceding title; frame 1704 begins the black-to-cabin fade. All 120 S27 frames reviewed in sequence on a contact sheet; cabin composition continues through the lighting reveal to frame 1823 and EOF. Duration 5.000s; reveal is a lighting change within S27. | PASS |
| Card at 5s, frame 120 | A NEW DOCUMENTARY BY NATHAN FIELDER — exact plan text. | PASS |
| Card at 63.75s, frame 1530 | THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE — exact plan text and line breaks. | PASS |
| SRT unchanged from v7 | Byte-identical, 705 bytes each; SHA-256 `5b2c8806b9eadd6363f3d7a9140fac2ab18a1351ba9b4d8434da782d6f59db06`. | PASS |

**Updated overall verdict: FAIL full-spec QC — one remaining exterior styling issue.** Score-stem silence and touchscreen styling now pass; all requested audio and regression checks pass. The previously completed full duration audit remains PASS (minimum 2.000s); the focused S27 recheck confirms its 5.000s duration. Exterior detail remains visible before the headlight reveal. No production assets changed.


## Re-QC 2 — 2026-10-18

Final targeted verification only, following the preceding Re-QC's sole remaining exterior failure. No production assets changed. This section supersedes the prior verdict for the items rechecked below; earlier broader checks are carried forward, not rerun.

Artifact: `you-can-see-anything-teaser-v10.mp4`, 32,114,327 bytes. SHA-256: `4cecd8d5bf6241088f74255f39d3ebb7627808facba5247bf8850d84c142e084`.

Method: decoded the MP4 from the beginning, extracting each zero-based frame with FFmpeg `-vf 'select=eq(n\,N)' -frames:v 1 -fps_mode vfr`; no time-seeking. Inspected the original full-resolution PNGs without exposure or contrast adjustment. Extracts are in `/tmp/reqc2-v10/frame_N.png`.

### Targeted picture checks — FAIL (residual pre-switch glow)

| Frame / time | Observation | Result |
|---|---|---|
| 1740 / 72.500000s | Exterior reads effectively black; no recognizable building mass, glow band or readable signage. Dash/wheel and cabin trim remain visible as expected. Touchscreen is black with white YOU CAN SEE / EVERYTHING. | PASS |
| 1780 / 74.166667s | Exterior still reads effectively black, with no recognizable frontage or readable signage; expected interior and black title screen remain. | PASS |
| 1786 / 74.416667s | Substantially darker than the prior reported version, but a faint horizontal gray/brown exterior glow band remains visible in the central windshield, approximately x=650–1120, y=340–380 in the 1920×1080 frame, above the blue dash edge. Very faint blocky exterior shapes remain above it; no readable signage. These are outside the cabin. The requested **no glow band** criterion is not met. | **FAIL** |
| 1787 / 74.458333s | Headlights on: food-bank frontage, FOOD BANK sign and wet ground clearly illuminated through the windshield. Cabin/wheel/dash/viewpoint continue across 1786→1787; touchscreen remains black with the white title. | PASS |
| 1823 / 75.958333s | Food bank remains lit through the windshield at the final frame; same composition with natural small viewpoint movement, and black touchscreen with white title. | PASS |

### Regression — PASS

| Check | Evidence | Result |
|---|---|---|
| Total frames / runtime | FFprobe decoded count 1,824 at 24/1 fps; video, audio stream and container durations 76.000000s. | PASS |
| S27 boundary | Frame 1703 retains the full-frame title; frame 1704 (71.000000s) is black at the start of the cabin fade. Boundary intact. S27 remains frames 1704–1823 inclusive: 120 frames / 5.000s. The existing complete duration audit remains applicable, minimum 2.000s / 48 frames. | PASS |
| PCM mix silence 65–67s | `build/v10/audio_mix.wav`: 48 kHz, 3,648,000 samples; samples 3,120,000–3,215,999 inclusive all exactly zero (0/96,000 nonzero). Score stem also has 0/192,000 nonzero channel samples in this interval. | PASS |
| Title onset | First sample above −50 dBFS after 67s: PCM mix 67.002021s; decoded MP4 audio 67.001938s. Both within 67.002 ±0.010s and match prior measurements. | PASS |
| Audio regression against prior measured values | Mix peak −0.305642 dBFS, mix 75–76s RMS −71.411856 dBFS, score tail RMS −73.302555 dBFS and score onset 67.001875s all match the prior Re-QC. Encoded gap retains the previously reported AAC edge residue: 1,216 nonzero decoded samples, peak 0.000396422; exact zero applies to the PCM mix. No audio regression detected in the requested checks; no claim of byte identity to an unavailable prior MP4. | PASS |

**Updated overall verdict: FAIL — one remaining pre-switch exterior styling issue at frame 1786.** The windshield blackout is improved, but the residual exterior glow band fails the explicit no-glow-band requirement. Post-switch reveal, black title touchscreen, runtime/frame count, S27 boundary and requested audio regressions pass. The earlier broader QC passes remain carried forward. Verification only; only this report was modified.


## Re-QC 3 — 2026-10-18

Final confirmation, verification only. Read Re-QC 2 and checked the rebuilt rendered artifact. Only this report was modified; no production assets changed. This section supersedes the earlier overall FAIL verdict. Earlier broader QC passes and their stated measurement qualifications are carried forward, not rerun.

Artifact: `you-can-see-anything-teaser-v10.mp4`, 32,095,800 bytes. SHA-256: `ae01c2b3220d4031989e5b8d5098f43a77edbea5518826cabd687072b8239bfa`.

Method: FFmpeg sequential decode from the beginning, selecting zero-based indices with `select=eq(n\,1740)+eq(n\,1780)+eq(n\,1786)+eq(n\,1787)` and `-fps_mode vfr`; no time-seeking. Full-resolution 1920×1080 PNGs inspected without exposure/contrast adjustment. Extracts: `/tmp/reqc3-v10/selected_01.png` through `selected_04.png`, in that index order. Measurements: `/tmp/reqc3-v10/measurements.json`.

Pixel measurements are decoded PNG RGB code values on the 0–255 scale. Mean is over all pixels and all three channels; maximum is over the same values. Coordinates are start-inclusive/end-exclusive. The broad windshield ROI is x=[0,1920), y=[0,460), entirely above the touchscreen. The former glow-band ROI is x=[650,1120), y=[340,380). Each pre-switch ROI is exactly zero in every channel.

| Frame / time | Windshield RGB mean / max | Former band RGB mean / max | Visual finding | Result |
|---|---:|---:|---|---|
| 1740 / 72.500000s | 0.000000 / 0 | 0.000000 / 0 | No exterior glow band, building mass or signage visible. Black touchscreen with white title intact. | PASS |
| 1780 / 74.166667s | 0.000000 / 0 | 0.000000 / 0 | No exterior glow band, building mass or signage visible. Black touchscreen with white title intact. | PASS |
| 1786 / 74.416667s | 0.000000 / 0 | 0.000000 / 0 | Former residual band is absent; no exterior glow band, building mass or signage visible. | PASS |
| 1787 / 74.458333s | 85.371653 / 255 | 173.924876 / 255 | Headlight reveal intact: food-bank frontage, FOOD BANK sign and wet ground illuminated. Cabin composition continues; touchscreen remains black with white YOU CAN SEE / EVERYTHING. | PASS |

### Regression — PASS

| Check | Measurement | Result |
|---|---|---|
| Decoded frame count / runtime | FFprobe `-count_frames`: 1,824 decoded frames, 1920×1080, 24/1 fps; video, audio stream and container durations 76.000000s. | PASS |
| PCM mix 65–67s exact zero | `build/v10/audio_mix.wav`: mono signed 16-bit, 48,000Hz, 3,648,000 samples (76.000s). Samples 3,120,000–3,215,999 inclusive: 0/96,000 nonzero, absolute peak 0. | PASS |

Exact digital zero refers to the PCM mix, consistent with prior QC; this check does not assert bit-zero AAC decoding.

**Final overall verdict for v10 QC: PASS.** Re-QC 2's sole remaining failure—the pre-switch exterior glow band at frame 1786—is resolved, with exact black measured across the windshield in all three requested pre-switch frames. Reveal, title screen, total frames/runtime and PCM mix gap pass. The earlier full duration audit remains PASS, minimum 2.000s / 48 frames, with the other previously passed QC items carried forward. No full broader QC rerun is claimed.
