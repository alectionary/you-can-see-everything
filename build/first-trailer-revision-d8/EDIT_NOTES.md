# D8 — user editorial revision

[Published on YouTube as YOU CAN SEE EVERYTHING TRAILER #1](https://youtu.be/ZXksQL-8OBw) (public).

Viewing copy: `build/first-trailer-revision-d8/first-trailer-revision-d8.mp4`.

Runtime is 3:17. The third rehearsal gains four seconds and the Times Square reveal gains two; no existing shot is shortened. D7 and earlier exports are preserved. This pass uses existing character video and accepted speech, plus three built-in GPT-generated settings. No new Runway or ElevenLabs generation was used.

## Fifteen requested changes

| Request | D8 result | New time |
|---|---|---|
| 1. Remove the nauseating shaky stills | The rear interview and communications photographs are replaced by locked title cards. Other requested screen reveals use a single smooth subpixel pullback, with no artificial shake or stepped `zoompan`. | 0:44–0:52; 1:11–1:16 |
| 2. Stop showing Roy playing after 0:12; restore the simultaneous joke | **YOU CAN SEE THE TRUTH** fills 0:12–0:18 and the clean Roy instrument stops at 0:12. Dan and Nathan are side by side during the assurance. The same Dan image sequence and identical accepted audio recur twice; only Nathan's reaction performance changes. The squint anchors are on “that,” approximately 0:21.30, 0:27.30 and 0:31.30. The original “Again” remains before the second take. The third take then includes the existing “Was the first one too suspicious?” | 0:12–0:38 |
| 3. Keep lookalikes moving; reveal the composing board on a glary MacBook | Candidate A begins as moving video and smoothly pulls out to the photographed MacBook. Candidates B and C continue as moving playback in its editing interface. Window reflection/fingerprint texture stays fixed to the glass. | 0:52–1:06 |
| 4. Fix the 1:50 strumming mismatch | The first six seconds of the continuous Roy source show his introduction, resting hand and opening/damping gesture, so no strum cue plays there. Clean string attacks during actual playing follow reviewed hand-motion peaks from that same source. Opening, apology and final playing receive the same source-based treatment. Pluck/body underscore is suppressed during the idle introduction. | Introduction 1:52–1:58; playing 1:58–2:06 |
| 5. Change Pinterest handle | CTA reads **@YOU_CAN_SEE_EVERYTHING**, with exact underscores. | 3:13–3:17 |
| 6. Confusion exchange as Pinterest DMs on an iPhone | The existing Dan recording appears as an incoming message, “I thought you looked confused.” Nathan replies “I was.” Message arrivals follow the accepted voice timings. | 0:38–0:44 |
| 7. Refusal/lookalike exchange over title | **YOU CAN SEE A CHARACTER HE CREATED** replaces the interview photograph; both accepted voice lines remain. | 0:44–0:52 |
| 8. Corporate communications title | **YOU CAN SEE CORPORATE COMMUNICATIONS** replaces the woman's still while preserving her factual-accuracy line. | 1:11–1:16 |
| 9. Parking title before lot | **YOU CAN SEE PARKING** now precedes the actual rainy empty-lot footage. The lot retains all three seconds and its existing question. | Title 1:20–1:22; lot 1:22–1:25 |
| 10. Friendly planning image under “Which version…” | A reassuring pencil/CAD/watercolor parking scheme shows trees, rain gardens and the food-bank ghost outline, with a demolition-permit inset. | 1:25–1:28 |
| 11. Trolling card instead of clappers | **YOU CAN SEE TROLLING** replaces the guest shot, with existing audio preserved. | 1:40–1:44 |
| 12. Dan's Pinterest post | A moving embedded copy of the Picasso destruction sits in Dan's post, with heart, laughing, surprised and angry reactions. The angry counter reads **9,999,999,999+**, dwarfing the others. His Pinterest-distribution line remains on the soundtrack. | 1:44–1:50 |
| 13. Arrangement exchange as DMs, then block | Nathan asks “Did you arrange this?” Dan replies “Roy chose the song.” The phone is Dan's view of the Nathan thread, ending with **YOU BLOCKED NATHAN**. | 2:06–2:14; block appears 2:12.35 |
| 14. Nathan's post reveal | The Nathan/editor image pulls back into a Pinterest post authored by Nathan with the text **I didn’t know.** The reveal begins as his existing line arrives. | 2:20–2:26 |
| 15. Roy/lawyer DM becomes Times Square billboard | A readable private-message screenshot includes the lawyer's “Did you authorize this?” and Roy's interrupted line. The camera pulls out to reveal the screenshot on a giant Times Square billboard, with two seconds to hold the public display. The ominous score is extended under the longer reveal. | 2:48–2:54 |

The existing Dan signature line remains visibly Dan, entirely before Roy's separate interrupted response. Worn Pinterest documents, food-bank footage, escalating BEYOND TRUTH/EVERYTHING cards, the two-second black/silent beat and the final Pinterest reply are retained at their shifted positions.

## Saved sources and prompt set

Built-in imagegen produced these three project assets; exact prompts and SHA-256 hashes are in `images/provenance.json`:

- `trailer/first/revision-d8/images/macbook.png`
- `trailer/first/revision-d8/images/plan.png`
- `trailer/first/revision-d8/images/times_square.png`

Pinterest posts, messages, phone frames, reaction icons and title cards are editable native artwork in `build_revision.py`. They are fictional in-universe interfaces. `build/first-trailer-revision-d8/hand-motion.json` records source frames, optical-flow measurements, reviewed gesture exclusions and final attack times. `rehearsal-sync.json` records the repeated Dan source and the reaction anchors. The MIDI retains measured frame timing; printed Roy notation rounds to quarter-second subdivisions for readability. All score colors/timbres continue to derive from the existing ukulele sample recordings.

## Rebuild and QC

Use the existing finishing Python environment, ffmpeg, LilyPond and Poppler:

```sh
python trailer/first/revision-d8/analyze_hand_motion.py
python trailer/first/revision-d8/build_revision.py prepare compose audio picture export
python trailer/first/revision-d8/build_score.py
python trailer/first/revision-d8/verify_revision.py
```

The picture stage resumes existing D8 segments. Deliberate source/render changes require rerendering the affected D8 segment or its named builder before `picture export`. No network API is called on rebuild. All underlying accepted character clips and voice files remain local.

`build/first-trailer-revision-d8/QC.md` contains the explicit RULES.md audit and all 44 actual segment durations; minimum is 2.000 seconds. The new cards over spoken lines, replays and dialogue repositioning are explicitly authorized by this revision request. Final MP4 checks cover decoded audio, exact Dan PCM copies and repeated picture frames, simultaneous reaction sources, stable title pixels, moving audition playback, the block banner, hand-led strum attack timing, black/silence, loudness, pitch, MIDI, score compilation and scene cuts. Actual-output contact sheets cover the fifteen visual edits. Generated fingering remains approximate; no subjective headphone/speaker listening approval is claimed.
