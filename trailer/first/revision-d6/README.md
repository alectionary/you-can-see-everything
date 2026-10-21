# D6 user-notes revision

Completed alternate: `/Users/anonymous/Documents/you-can-see-anything-teaser/build/first-trailer-revision-d6/first-trailer-revision-d6.mp4`.

Runtime is **191 seconds / 3:11**. Forty original holds retain their durations; four cards add eleven seconds. D4 and D5 remain intact. Technical checks pass on the actual delivered MP4. No Runway calls or new ElevenLabs requests were made. Three document props were generated with the built-in image-generation tool.

## Requested changes

- Roy's opening now has clearly ringing four-string down-strums rather than thin isolated plucks. Staggering the strings by 13 ms creates the strum; the original wrong chord, damping and restart remain. Opening instrument RMS is 5.49 dB above D5. No other musical bus plays before 18 seconds; the restart yields smoothly to the interview question. The continuous middle ukulele performance remains unchanged after its four-second timeline shift.
- T04 restores both original Dan recordings: “Why would I deceive you?” at 18.400, then “There's no reason for me to do that” at 20.250. Both are the established Dan/Eric voice from the teaser. The recorded durations are natural; no new voice was generated. The new question and moved assurance each have a matching spoken subtitle.
- Dan's six visible speaking shots (T04, T08, T10, T22, T26, T30) now use a tracked neutral lower-mouth pose outside his actual speech windows, settling within 100 ms. Eyes, brow, head and body remain live. T04's speaking mouth is re-driven from the restored two-sentence audio. The profile table shot has its own offset mask and reference. The actual final MP4 was checked against the saved neutral patches and original upper-face motion. Mouth detail during speech remains synthesized and is not certified phoneme-perfect.
- Three clean document inserts are replaced with handled photographic props. T14 is a folded, coffee-ringed preparation printout; T29 is a glary phone photo of a communications-review monitor; T33 is a scuffed discarded distribution printout. Key wording remains legible. These are fictional in-universe production props.
- Standalone black cards build through YOU CAN SEE PARKING, YOU CAN SEE BETRAYAL, YOU CAN SEE BEYOND TRUTH and the larger YOU CAN SEE EVERYTHING title. The final card reads LEARN MORE ON PINTEREST / @YOUCANSEEEVERYTHINGFILMS. This is in-film typography; no account was created or published.
- Score events, sustained textures, bass pulses and instrument-body rhythm are extended through the new cards. The whole soundtrack and voices were not stretched. The PDF, eight-track MIDI, event JSON/CSV and ten PCM stems all follow the 191-second timeline.

## Added cards and final timing

| Composition | Start | End | Duration |
|---|---:|---:|---:|
| YOU CAN SEE PARKING | 79 | 81 | 2 |
| YOU CAN SEE BETRAYAL | 106 | 108 | 2 |
| YOU CAN SEE BEYOND TRUTH | 168 | 171 | 3 |
| Exact black / silence | 171 | 173 | 2 |
| YOU CAN SEE EVERYTHING title | 173 | 177 | 4 |
| Roy question / Pinterest reply | 177 | 187 | 10 |
| LEARN MORE ON PINTEREST | 187 | 191 | 4 |

The title has one shared attack at 173. Music ends by 177. The final CTA is deliberately silent after Roy's room scene. Original Fielder reaction T05 is retained, including the specific squint/downward glance; no original shot is shortened to accommodate a card. Every card is clear of spoken subtitle windows.

## Media, score and checks

All outputs below are inside `/Users/anonymous/Documents/you-can-see-anything-teaser/build/first-trailer-revision-d6/`:

- `first-trailer-revision-d6.mp4`: H.264 1280 x 720, 24 fps; stereo 48 kHz AAC. Review label is updated to D6 on ordinary shots.
- `mix.wav`: full stereo 48 kHz / 24-bit master. Encoded delivery is -18.03 LUFS, -1.80 dBTP, 11.60 LU range.
- `music-only.wav`: unmastered music at mix balance.
- `stems/`: roy, plucks, low, bloom, grit, body, reverse, dialogue, effects, ambience; each exactly 9,168,000 stereo PCM frames.
- `audio-review/`: opening/restored Dan, parking card, betrayal/Pinterest section and ending/card excerpts.
- `score/ukulele-score-d6.pdf`, adjacent editable `.ly`, complete `.mid`, seven role `.mid` files, `events.json`, `event-cues.csv` and compile log. Six A3 pages, four seconds per 4/4 bar, final three-beat bar. Complete MIDI marks the final 3/4 meter at 188 seconds.
- `timeline.csv`, `dialogue.csv`, `captions.srt`, `speech/timing.json`: exact current edit and speech/caption map.
- `mouths/` and `mouth-corrections.json`: timing masks, tracking transforms, neutral references, model/output hashes and per-shot audit.
- `QC.json`, `QC.md`: actual video duration/frames, all 44 segment durations, decoded silence/black, pitch, loudness, mono compatibility, restored Dan speech-source correlations, sampled silent-mouth checks and full scene scan. All detected cuts match planned boundaries within a frame; there is no unplanned internal cut.
- `VISUAL_REVIEW.md`: actual final frames and score page review; this does not claim human headphone/speaker listening approval.

## Document images and exact prompts

Generated with the built-in `image_gen.imagegen` tool in three reference-edit calls, using the corresponding D3 native plates. Final project-bound assets are:

- `/Users/anonymous/Documents/you-can-see-anything-teaser/trailer/first/revision-d6/images/T14.png`
- `/Users/anonymous/Documents/you-can-see-anything-teaser/trailer/first/revision-d6/images/T29.png`
- `/Users/anonymous/Documents/you-can-see-anything-teaser/trailer/first/revision-d6/images/T33.png`

`images/provenance.json` contains the complete final prompt for each image, original source reference, saved output path and SHA-256. Original generated files remain at their default generated-images location as well; delivery uses the durable repository copies.

## Reproduction

Use `/private/tmp/ycs-finishing-venv/bin/python`, FFmpeg, LilyPond and the existing local Wav2Lip checkout/checkpoint for T04's mouth regeneration. The runtime dependencies and model terms/provenance remain saved under `trailer/first/finishing-d4/`. This continues the user's personal/noncommercial workflow. No model/API is required if the saved corrected mouth videos and document PNGs are retained.

```sh
/private/tmp/ycs-finishing-venv/bin/python trailer/first/revision-d6/build_revision.py prepare compose score audio
/private/tmp/ycs-finishing-venv/bin/python trailer/first/revision-d6/correct_mouths.py
/private/tmp/ycs-finishing-venv/bin/python trailer/first/revision-d6/build_revision.py picture export
/private/tmp/ycs-finishing-venv/bin/python trailer/first/revision-d6/verify_revision.py
```

The default renderer runs all stages in that same order. Picture segments and mouth corrections are cached; remove only the relevant D6 cached output before changing its source. Never remove or rewrite D4/D5 comparison outputs. After notation edits, render the PDF and inspect its pages again. No Git commit or push has been made.
