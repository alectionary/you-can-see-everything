# YOU CAN SEE EVERYTHING — v10 build plan

RULES.md outranks this plan. This replaces the v8 plan and v9 revision in EDIT_PLAN.md. Runtime is **71.000 seconds / 1,704 frames at 24fps**, 1920×1080. Times are seconds, start-inclusive/end-exclusive; all picture boundaries are integral frames. There is no target-length compression. All visible segments, including every panel composition and card reveal, are enumerated below; no hidden microcuts or changing panels inside these intervals.

## Sources and assembly

Use original, unsubtitled pictures, with source seconds measured from each file's start; strip their production audio. Resolve each wildcard below to its single existing MP4 (fail if missing or ambiguous):

| Key | Existing source |
|---|---|
| F01 | clips/v2/*shot01-*.mp4 |
| D02 | clips/v3/*shot02-*.mp4 |
| D03 | clips/v3/*shot03-*.mp4 |
| ROY | clips/v4/*shot04-*.mp4 |
| D05 | clips/v3/*shot05-*.mp4 |
| D06 | clips/v3/*shot06-*.mp4 |
| REACTION | clips/v4/*fielder-reaction-*.mp4 |
| SEDAN | clips/inserts/*rainy-lot-sedan-*.mp4 |
| FOOD | clips/inserts/*food-bank-*.mp4 |
| LOT | clips/inserts/*empty-lot-after-*.mp4 |
| DEMO | clips/inserts/*demolition-*.mp4 |

F01: use v7's glitch correction (trim first .350s, prepend .350s clone) before applying listed source ranges. ROY: use v7's first-.300s correction the same way. All other source ranges refer directly to originals. Match existing v7 crops: F01 scale 1920×2880/crop y420; ROY and REACTION scale 1920×2880/crop y700; Dan sources scale 1920×1920/crop y420; all crops 1920×1080. Inserts scale to 1920×1080. Panel crops keep mouths and required character details visible. No temporal offsets between duplicated face tiles. D06's later silent source reuse is intentional; cut only at listed boundaries, with no loops or resets inside a segment.

Use the eleven dialogue/v2 MP3s with unchanged v7 delays: f01 1.500, d01 8.000, f02 14.500, d02 18.000, f03 23.000, r01 26.000, d03 32.000, d04 35.000, d05 37.500, f04 42.500, d06 45.000. Copy build/v7/teaser.srt verbatim; burn once after compositing. Speech times below are the exact SRT windows, not SCRIPT.md delivery slots. Preserve ordinary performances and existing character canon.

## Complete segment table

| ID | Start | End | Duration | Picture content / source | Dialogue (exact SRT times) |
|---|---:|---:|---:|---|---|
| S01 | 0.000 | 4.000 | 4.000 | Full-frame Fielder; F01 source 0–4. | And the county approved the parking? (00:00:01,500–00:00:03,265) |
| S02 | 4.000 | 6.000 | 2.000 | CARD 1 — A NEW DOCUMENTARY BY NATHAN FIELDER | — |
| S03 | 6.000 | 8.000 | 2.000 | Full-frame SEDAN source 1–3; wordless pre-answer pause. | — |
| S04 | 8.000 | 10.000 | 2.000 | Full-frame Dan; D02 source 2–4, synced to locked answer. | The use was permitted. (00:00:08,000–00:00:09,161) |
| S05 | 10.000 | 12.500 | 2.500 | Full-frame LOT source 2–4.5. | — |
| S06 | 12.500 | 14.500 | 2.000 | Full-frame silent Dan; D03 source 0–2, continuous take. | — |
| S07 | 14.500 | 17.000 | 2.500 | Full-frame FOOD source 1–3.5; Fielder offscreen. | The building was a food bank. (00:00:14,500–00:00:16,125) |
| S08 | 17.000 | 20.000 | 3.000 | Full-frame Dan; D03 source 3–6, synced at 18. | I can't account for their interpretation. (00:00:18,000–00:00:19,858) |
| S09 | 20.000 | 22.000 | 2.000 | CARD 2 — AN EXTRAORDINARY ACT OF LISTENING | — |
| S10 | 22.000 | 27.000 | 5.000 | Two panels: REACTION source 0–5 left; ROY source 0–5 right. Roy visibly speaks; preserve hoodie, thin Filipino silhouette and crutches. | It says here the neighbors objected. (00:00:23,000–00:00:24,950)<br>Never. Not once. (00:00:26,000–00:00:26,975) |
| S11 | 27.000 | 30.000 | 3.000 | Two panels: DEMO source 3–6 left; ROY source 5–8 right. Swap left panel at 27.000 (first 24fps frame after 26.975); no intervening composition. | — |
| S12 | 30.000 | 32.000 | 2.000 | CARD 3 — A BRAVE NEW LANGUAGE OF TRUTH | — |
| S13 | 32.000 | 34.500 | 2.500 | Two panels: Dan dominant 1280px, D05 source 2–4.5; REACTION source 0–2.5 in right 640px. Dan visibly speaks through 34.136. | I'm engaging with you as a human being. (00:00:32,000–00:00:34,136) |
| S14 | 34.500 | 39.500 | 5.000 | Three panels: FOOD source 4–9 left 480px; mouth-closed REACTION source 0–5 center 960px; LOT source 5–10 right 480px. No Dan image anywhere. | Why would I deceive you? (00:00:35,000–00:00:36,161)<br>There's no reason for me to do that. (00:00:37,500–00:00:39,265) |
| S15 | 39.500 | 42.000 | 2.500 | CARD 4 — CINEMA WILL NEVER BE THE SAME | — |
| S16 | 42.000 | 47.000 | 5.000 | Split stare: D06 source 0–5 duplicated simultaneously; 8px vertical seam displacement. Dan visibly answers; Fielder offscreen. | Are you being real right now? (00:00:42,500–00:00:44,125)<br>I'm always being real. (00:00:45,000–00:00:46,161) |
| S17 | 47.000 | 49.000 | 2.000 | 2×2 Dan grid: D06 source 5–7, simultaneous tiles; offsets 4–8px, modest scale mismatch. | — |
| S18 | 49.000 | 51.000 | 2.000 | CARD 5 — BEYOND TRUTH. BEYOND CINEMA. | — |
| S19 | 51.000 | 54.000 | 3.000 | 3×3 Dan grid: D06 source 7–10, simultaneous tiles; offsets to 12px, recognizable central direct lens contact. | — |
| S20 | 54.000 | 56.000 | 2.000 | CARD 6 — A WORK OF IMPOSSIBLE GENIUS | — |
| S21 | 56.000 | 58.500 | 2.500 | 4×4 mixed grid: D06 source 7–9.5 simultaneously in face cells; LOT source 5–7.5 in cell 5, DEMO source 3–5.5 in cell 10 (zero-based row-major); offsets to 20px. | — |
| S22 | 58.500 | 60.500 | 2.000 | CARD 7 — A POSTMODERN MASTERPIECE | — |
| S23 | 60.500 | 62.500 | 2.000 | 4×4 mixed grid continues same geometry; D06 source 5–7 simultaneously in face cells; LOT source 7.5–9.5 and DEMO source 5.5–7.5 in cells 5 and 10. | — |
| S24 | 62.500 | 65.000 | 2.500 | CARD 8 — THE GREATEST FILM YOU WILL EVER SEE IN YOUR LIFE | — |
| S25 | 65.000 | 67.000 | 2.000 | Pure black, no text; absolute digital silence on every audio bus. | — |
| S26 | 67.000 | 71.000 | 4.000 | Static title YOU CAN SEE EVERYTHING; one fff ensemble chord at first frame, externally decayed through end. | — |

## Cards, escalation and sound

Cards replace the full frame, white centered restrained sans-serif on pure black; exact wording above, no attribution, speech or sound effects. Sizes increase across cards, with reduced margins; keep all text inside 90% safe area. Card 8 breaks as “THE GREATEST FILM / YOU WILL / EVER SEE IN / YOUR LIFE”, held 2.500s. Title uses Liberation Sans Regular 64, color 0xE6E4DF, centered, no animation or end fade.

Clear-film gaps between successive cards are **14.000, 8.000, 7.500, 7.000, 3.000, 2.500, 2.000 seconds**, strictly decreasing. Card durations are 2, 2, 2, 2.5, 2, 2, 2, 2.5 seconds; acceleration comes from the gaps and increasing panel density. The sequence is clean full-frame → two-panel → three-panel reaction → split stare → 2×2 → 3×3 → 4×4 → card 8 → black/silence → title. Card 4 replaces the obsolete quarter-second Dan return; the demolition composition holds until card 3, removing the obsolete Roy sliver. No unseen extra grid or return composition is required under a card.

Score10 keeps A–C (0–42) unchanged, retains the original D through 55, and adds ten quarter notes of cluster/tremolo/irregular-group development through 65. All-staff rest is 65–67; one fff title attack is at 67, held to 71 with an external exponential envelope (tau approximately 1.2s). No extra attacks or end tail. Disable synth chorus/reverb. Duck music about 6dB under locked speech, preserving consonants. Keep room tone through 65 only. Gate every bus and synth release to exact PCM zeros for 65–67: 48kHz samples 3,120,000 through 3,215,999 inclusive. Trim at sample 3,408,000. The black beat is two full seconds; no part of it funds card 8.

## Rules and verification brief

Rule 1: the exhaustive audit below covers every actual visible shot, insert, card, panel/grid composition, black beat and title. Rule 2: added holds extend runtime to 71; no shortening of black or title to preserve an old runtime. Rule 3: all eleven SRT windows stay fixed, all eight cards avoid speech, Dan remains visible during on-camera lines, both deceive-you lines have only Fielder's closed-mouth reaction plus wordless inserts, and the food-bank insert covers the 14.500 line. Sedan ends exactly at 8.000 before the answer; demolition swaps at 27.000 after Roy.

Rule 4: run `python3 score/verify_score10.py`; it prints each duration, card/SRT overlap checks, preserved A–C checks and LilyPond's evaluated part lengths, compiling only to a temporary directory. Rule 5 is a required future rendered-artifact QC gate, not a claim of rendered verification here: no video or audio is built for this planning task. Before any future delivery, inspect the actual output's 1,704 frames, every listed boundary, mouth sync and closed-mouth reactions, source continuity, exact subtitles, title frame 1,608, music pitch/levels, single title attack, sample-zero interval and trimmed tails. Inspect the encoded viewing copy as well as the PCM master.

## DURATION AUDIT

Required minimum for **every segment: 2.000 seconds**; card 8 additionally ≥2.500s, black ≥2.000s, title ≥4.000s.

| Segment | Duration (s) | Minimum (s) | Result |
|---|---:|---:|---|
| S01 | 4.000 | 2.000 | PASS |
| S02 | 2.000 | 2.000 | PASS |
| S03 | 2.000 | 2.000 | PASS |
| S04 | 2.000 | 2.000 | PASS |
| S05 | 2.500 | 2.000 | PASS |
| S06 | 2.000 | 2.000 | PASS |
| S07 | 2.500 | 2.000 | PASS |
| S08 | 3.000 | 2.000 | PASS |
| S09 | 2.000 | 2.000 | PASS |
| S10 | 5.000 | 2.000 | PASS |
| S11 | 3.000 | 2.000 | PASS |
| S12 | 2.000 | 2.000 | PASS |
| S13 | 2.500 | 2.000 | PASS |
| S14 | 5.000 | 2.000 | PASS |
| S15 | 2.500 | 2.000 | PASS |
| S16 | 5.000 | 2.000 | PASS |
| S17 | 2.000 | 2.000 | PASS |
| S18 | 2.000 | 2.000 | PASS |
| S19 | 3.000 | 2.000 | PASS |
| S20 | 2.000 | 2.000 | PASS |
| S21 | 2.500 | 2.000 | PASS |
| S22 | 2.000 | 2.000 | PASS |
| S23 | 2.000 | 2.000 | PASS |
| S24 | 2.500 | 2.500 | PASS |
| S25 | 2.000 | 2.000 | PASS |
| S26 | 4.000 | 4.000 | PASS |

Total: **71.000s**. Smallest segment: **2.000s**. All 26 segments pass; no exceptions.
