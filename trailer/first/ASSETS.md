# First full trailer asset checklist

Draft 1. Reuse the existing pictures below; new cinematic coverage is required for the rehearsal, casting, ski lodge and stream. Screen graphics are authored in the edit so names, comments and playback remain exact. No provider/model provenance is asserted from the existing download host.

## Existing footage measured locally

| ID | Source | Duration | Native dimensions | Used in | Assembly note |
|---|---|---:|---|---|---|
| E01 | `clips/v3/media-generation-v3-shot05-dan-deceive-0-a98fda19-a4f1-4fac-91cb-7979397f402f.mp4` | 10.000s | 960×960 | T04 | Dan hold source 0–4, under the d05 assurance as voiceover; no mouth-sync claim. |
| E02 | `clips/v4/media-generation-v4-fielder-reaction-0-f0f2b96c-6673-45ea-abf0-fc41e81a9275.mp4` | 10.000s | 768×1152 | T05 | Exact squint and downward glance from v10 at about 39s. Source 2–6 includes it; source 0–4 misses it. |
| E03 | `clips/inserts/media-generation-insert-food-bank-0-b6ef9a19-92ea-4eae-8b2e-ee2e9dac6c06.mp4` | 10.000s | 1280×720 | T16 | Functioning food bank, source 1–5. |
| E04 | `clips/inserts/media-generation-insert-empty-lot-after-0-1d5e3578-9d88-49b6-adde-4b9b449108fc.mp4` | 10.000s | 1280×720 | T17 | Empty lot, source 2–5. |
| E05 | `clips/inserts/media-generation-insert-demolition-0-e4ec74c2-afbd-4b2e-a5aa-bdb9c497b7cb.mp4` | 10.000s | 1280×720 | T32 T33 | Demolition source 3–6; extract the presentation still from this interval. |

## Recorded dialogue available

- L04: `dialogue/v2/d05.mp3` — “There’s no reason for me to do that.” Existing locked subtitle duration is 1.765s; new target window is 18.400–20.165.
- L29: `dialogue/v2/d03.mp3` — “I’m engaging with you as a human being.” Existing locked subtitle duration is 2.136s; new target is 158.200–160.336.
- `dialogue/v2/r01.mp3` contains the original “Never. Not once.” It can guide restrained delivery; it does not supply the candidates’ new “No. Not once.” lines.

The existing MP3s may include encoder padding or leading silence. Measure active speech before placing them; the subtitle spans above are speech targets, not file durations.

## New character and location coverage

| ID | Needed material | Used in | Continuity and practical approach |
|---|---|---|---|
| N01 | Real Roy’s stream: setup, apology, restart, introduction, glance, final question and held reaction | T01–T03, T23–T24, T31, T39–T40 | One room, hoodie, ukulele, camera height and lighting. Record the musical master first. Capture matching shots with at least two-second handles; keep T39–T40 as one continuous ten-second take. These are coverage requirements, not a claim one generated clip can span the film. |
| N02 | Fielder’s alternative puzzled takes and two spoken remarks | T06–T07, T09 | Match E02’s chair, eyeline, light, blazer and framing. Rehearse the specific brow pinch, squint and dropped gaze at v10 ~39s. New takes must visibly reset and differ subtly; the current animatic labels its repeated-source stand-in. |
| N03 | New Dan interview answers | T08, T22, T26, T30 | Match E01’s actual screen identity and room. Batch the four new lines; avoid regenerating the two reusable recordings. |
| N04 | Dan and Fielder at the table outside the formal setup | T10 | Eight-second two-shot with natural refusal/proposal exchange. Additional handles if the performance needs them. |
| N05 | Three Roy candidates, separate interview takes | T11–T13, T35 | Three identifiable adults in similar wardrobe and identical interview setup. Candidate A must be the same person in N09. Casting differences are not an ethnicity joke. |
| N06 | Communications employee at the interview location | T15, T18 | Same staff identity and spatial position in both shots; factual, ordinary delivery. |
| N07 | Ski-lodge resort event, intact Picasso display, continuous shredding, guests | T19–T21 | Establish intact artwork before destruction. Use a fictional prop recreation for production. Clear physical continuity of canvas and mechanism; avoid rubbery generated destruction. Event is story canon; new coverage is a proposed depiction. |
| N08 | Dan watches Roy’s stream, with Fielder nearby, plus pullback plate | T24–T25 | Empty screen or trackable plate. Composite N01/G02 into it so the musical performance survives the reveal unchanged. |
| N09 | Candidate A with ukulele and offscreen crew response | T27 | Same actor as T11, same instrument style and casting location; no need to fake a skilled performance. |
| N10 | Fielder and editor reviewing the reaction | T28 | Readable monitor plate, match the room through screen light; G03 supplies accurate thumbnails. |
| N11 | Real Roy watching a monitor | T36 | Match N01’s Roy; do not substitute a candidate without explicitly changing the narrative. The unfinished line is his stream audio. |

## Graphics produced in the edit

| ID | Asset | Exact requirements |
|---|---|---|
| G01 | Corporate preparation document | SCRIPT.md T14 text, readable Pinterest identification, Primary destination: Pinterest, two comments, no real account data. |
| G02 | Stream interface and Pinterest wrapper | Modest stream audience; exact N01 playback; ROY FINDS HIS VOICE; final PINTEREST comment. Final comment is a separate five-second composition. |
| G03 | Editing interface and reaction thumbnails | Use actual E02 and accepted N02 stills; no nonsense text or unrelated faces. |
| G04 | Communications review screen | Interview preview, “Communications review,” “Use the earlier reaction.” |
| G05 | Pinterest distribution presentation | DISTRIBUTION STRATEGY; Keep the conversation on Pinterest; actual E05 frame, no fabricated metrics. |
| G06 | Black plate | 2.000 seconds at T37; all buses silent. |
| G07 | Title | Existing Liberation Sans Regular, restrained centered off-white lettering; 4.000 seconds. |

## Continuity images

`refs/DAN_v3.jpg`, `refs/ROY_v4.jpg`, `refs/FIELDER_v4.jpg`, and the specific `refs/FIELDER_reaction_39s.jpg` are extracted from the actual source videos. They are continuity references, not newly generated portraits. The original Fielder portrait also remains under the repository’s top-level refs/. Dan and Roy’s separate historical character-bible project is not present in this checkout; do not invent additional biographical details from that missing file.

## Audio to produce

- 20 new-trailer principal ElevenLabs performances are available; nine supporting cues still need production casting. L04 and L29 are the two preserved teaser recordings among 31 total lines.
- One original ukulele master with a believable error/restart and clean phrase; sample-accurate playback across the reveal.
- New piano, bass, string, brass and percussion stems following MUSIC_CUES.md; separate on-screen ukulele, room tone, shred mechanism, tentative applause and notification.
- Recovered ElevenLabs principal voices and settings are saved in voices.json: Dan/Eric, Roy/Chris, Fielder/Brian. Authentication and three new test generations pass; see VOICES.md. Supporting voices still need casting. The credential stays in Keychain.

## Production order

1. Assemble the placeholder animatic with the measured existing sources and these reference stills. Temporary voices can establish timing without paid synthesis.
2. Establish the ukulele phrase and extend the score’s notation around it; revise timings where performances need space.
3. Use the recovered principal voices and verified API access to render dialogue in short batches; establish separate supporting voices before their lines.
4. Confirm a video-generation or filmed-footage workflow. Existing metadata records do not provide a callable video service or model. Prepare still references and screen plates while that access is resolved.
5. Produce N01 first, then N08/G02. Their shared playback is the central continuity dependency. Produce rehearsal and casting next; lodge destruction is a separate effects task.
6. Replace placeholders, mix, and perform rendered-artifact QC against EDIT_PLAN.md.

## Asset status

The animatic is rendered under build/first-trailer-animatic/. All N assets still need production footage; G assets now have readable editorial mockups. New dialogue has temporary macOS voice recordings, and the music has an editable scratch score and rendered stems. The nylon-guitar timbre stands in for ukulele. D2’s 22 principal cues all use ElevenLabs or original teaser recordings. Nine supporting cues remain macOS placeholders. Provenance and credit usage are recorded in principal-dialogue-pass.json; see VOICE_PASS.md. See the rendered QC report for measured export checks and the remaining acting, lip-sync and listening review.

## First new rehearsal motion test

N02 now has one distinct generated test at clips/first/fielder-rehearsal-test-01.mov, with provenance beside it. The browser workflow confirms Runway Standard access. The result is 8.041667 seconds / 193 frames, 1280×720 at 24fps, silent. Its source 2–6 crop and the original reaction are available as a measured eight-second comparison under build/first-trailer-visual-tests-v1/fielder-motion-test/. Technical checks pass; the wider new framing and full performance still need creative review before replacing T06. The other N assets remain production requirements. See visual-tests/v1/README.md for the four continuity keyframes, screen proof, exact image prompts and motion shot cards.
