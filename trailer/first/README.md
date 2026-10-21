# First full trailer production package

## Published trailer #1 - D8

[Watch YOU CAN SEE EVERYTHING TRAILER #1 on YouTube](https://youtu.be/ZXksQL-8OBw) (public, published October 20, 2026).

The current cut is **3:17 / 197 seconds**, 1280 x 720 at 24 fps. [D8 edit notes](revision-d8/README.md) document all fifteen final editorial changes, the simultaneous Dan/Fielder rehearsal joke, hand-led ukulele timing, Pinterest messages/posts and Times Square reveal. [The saved viewing copy](../../build/first-trailer-revision-d8/first-trailer-revision-d8.mp4), [rendered QC](../../build/first-trailer-revision-d8/QC.md), [score](../../build/first-trailer-revision-d8/score/ukulele-score-d8.pdf), [MIDI](../../build/first-trailer-revision-d8/score/ukulele-score-d8.mid) and [publication record](../../build/first-trailer-revision-d8/youtube-publication.json) are versioned with the project.

Earlier workprints and the original teaser remain available below as production history.

Draft 1. YOU CAN SEE EVERYTHING. A separate 180.000-second trailer at 24 fps, 1920×1080; 4,320 frames. Prepared October 20, 2026.

Roy’s sincere effort to recover becomes material that the film and Pinterest can distribute. The trailer revisits the teaser’s apparent authenticity through rehearsed confusion, substitute Roys, corporate review, the Picasso destruction at Dan’s ski lodge, and a stream that widens into a Pinterest frame. The music carries Roy’s phrase into the teaser’s piano language, then into increasingly forceful bass and orchestral pressure.

## Production documents

- [Timed script](SCRIPT.md): dialogue, dramatic movements, readable screen text, and performance direction.
- [Edit plan](EDIT_PLAN.md): all 40 picture segments and the RULES.md audit.
- [Asset checklist](ASSETS.md): existing sources, new coverage, screen graphics, continuity images, and production order.
- [Music and sound cues](MUSIC_CUES.md): instrumental progression, original ukulele phrase, bass rhythm, and mix gates.
- [Timeline data](timeline.csv) and [dialogue data](dialogue.csv): machine-readable working timings for the animatic.

## Narrative commitments

Dan remains Pinterest’s CEO in this fictional continuity. His central interest is that Pinterest hosts the trends and conversations, including criticism and resistance. His personal virality is secondary; [STORY_CANON.md](STORY_CANON.md) records this distinction. The food-bank demolition succeeded. Roy’s streaming is part of his emotional recovery. The Picasso shredding takes place at Dan’s ski-lodge event. These are the user’s established story premises; the exact lines and arrangements here are proposed trailer scenes.

The film never proves Dan commissioned Roy’s song, the stream, or its critical content. His access to distribution and his ability to exploit an event are visible; omniscience is not established. Fielder’s rehearsal may expose manipulation while also participating in it. Roy’s refusal is meaningful even when production attempts to replace him.

The final PINTEREST comment is an authored fictional screen graphic. It is not a request to post, publish, or contact an account.

## Relationship to the teaser

This new trailer has its own dialogue timeline under the user’s request to develop a full trailer. The v7/v10 dialogue, subtitles, renders, and original build scripts remain untouched. Reused recorded lines retain their words and original performance, while their positions in this new film are specified here. This package does not claim that the new trailer has been rendered or has passed rendered-artifact QC.

## D2 principal voice pass

[Watch the latest voice pass](../../build/first-trailer-voice-pass-d2/first-trailer-voice-pass-d2.mp4). All 22 Dan, Roy and Fielder cues now use their recovered ElevenLabs voices, including two original teaser recordings. Nine supporting-role cues and the new footage remain placeholders. The [voice pass notes](VOICE_PASS.md) record the source manifest, credit usage, rebuild instructions and rendered checks. D1 is preserved separately.

## D1 animatic workprint

The [three-minute animatic](../../build/first-trailer-animatic/first-trailer-animatic-d1.mp4) combines the five reused source clips with labeled storyboard plates, readable corporate and Pinterest mockups, a continuous pullback mockup, 31 dialogue cues and a new scratch arrangement. Most new dialogue uses installed macOS placeholders; two Dan lines reuse existing recordings. The corrected platform-motive line uses the recovered ElevenLabs Eric voice. Voice-test and production-generation provenance is saved beside the relevant audio.

The plucked reference uses a nylon-guitar SoundFont as a temporary ukulele stand-in. New character acting, replacement Roy casting, lodge footage and the final ukulele performance remain to be produced. The footage has not been generated merely because its storyboard appears in the workprint.

- [Rendered QC report](../../build/first-trailer-animatic/QC.md) and [measurements](../../build/first-trailer-animatic/QC.json)
- [Editable music notation](../../build/first-trailer-animatic/score/first_trailer_score.ly) and [engraved score](../../build/first-trailer-animatic/score/first_trailer_score.pdf)
- [Scratch mix](../../build/first-trailer-animatic/mix.wav) and individual stems under build/first-trailer-animatic/stems/
- [Exported contact sheet](../../build/first-trailer-animatic/contact-sheet.jpg)

Measured export: 180.000 seconds, 4,320 frames, 1280×720 at 24 fps. Every source composition is at least two seconds; master and all PCM stems pass the exact 164–166 silence gate. The original teaser is unchanged. Acting, lip sync and dramatic balance remain production review tasks; this workprint is for reviewing structure, pacing and the musical direction.

## Established character voices

The [ElevenLabs voice configuration and samples](VOICES.md) recover Dan as Eric, Roy as Chris, and Fielder as Brian. Exact decoded audio matches confirm continuity with the teaser. The original Multilingual v2 model and per-voice settings are saved in voices.json. Three new samples generated successfully; D1 retains its temporary principal voices; D2 now uses the established ElevenLabs cast for every principal line.

## Rebuilding

Use the bundled Python with numpy and Pillow; ffmpeg, LilyPond, FluidSynth and macOS say must be on PATH. GeneralUser GS is loaded from the installed user Sound Banks folder. Launch from a local shell with access to the repository and installed voices:

```sh
/Users/anonymous/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 trailer/first/build_animatic.py --phase all
/Users/anonymous/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 trailer/first/verify_animatic.py
```

Phases prepare, audio and video can also run separately. Audio caches the synthesized lines by text and voice. To change the composition or MIDI, rerun prepare and remove the corresponding generated `score/*-raw.wav` before rerunning audio so cached SoundFont renders are not reused. The video phase rebuilds every segment and viewing copy.

## Next production work

Review the animatic’s holds and musical progression, then replace the stream, rehearsal and casting placeholders first. Keep N01’s exact performance inside the Pinterest reveal. If a new performance needs more space, extend the film and update all cue windows; do not borrow time from another established segment.

## Specific rehearsal reference

The rehearsal sequence targets [Fielder’s squint and downward glance at v10 about 39 seconds](REACTION_REFERENCE.md), following Dan’s “There’s no reason for me to do that.” T05 includes the exact source movement. The T06/T07 workprint repetitions are explicitly labeled stand-ins for new practice takes.

## Visual production tests v1

The [first two sequences now have continuity stills, motion prompts and separate visual tests](visual-tests/v1/README.md). The Roy reveal proof uses the same image continuously through Pinterest and into the viewing room; the Fielder reel pairs the actual reaction movement with clearly labeled new static pose references. These are compositing and continuity tests, not newly generated moving performances. D2-r1 remains the latest complete voice-pass trailer.

## Current visual production approach

Use ChatGPT’s built-in image generation for the next picture pass, with local camera moves, screen animation, compositing and suitable existing motion footage. Keep the established ElevenLabs voices and editable music. The available image tool creates stills; new actor motion and lip sync remain a later upgrade. The user has deferred further Runway generations. Preserve the saved rehearsal test and replace selected image-based shots with moving footage later if wanted. The working selection is recorded in production-mode.json.

## Full picture pass D3

The latest complete workprint is [first-trailer-picture-pass-d3.mp4](../../build/first-trailer-picture-pass-d3/first-trailer-picture-pass-d3.mp4). The three-minute cut now includes generated motion for Roy, the rehearsals, lookalike casting, communications, lodge shredding and Dan interviews, plus moving stream playback through the Pinterest reveal. All 31 voice cues use ElevenLabs or the established teaser recordings; accepted D2-r1 principal audio and score are preserved. Dan is identified on screen as Pinterest’s CEO.

This is a picture workprint. Exact dialogue-to-mouth synchronization, a final ukulele performance, and final sound polish remain open. See [D3 production notes](picture-pass-d3/README.md) and [rendered QC](../../build/first-trailer-picture-pass-d3/QC.md). The pass used 1,020 Runway credits, leaving 1,290.

## Finishing cut D4

Latest: [first-trailer-finishing-d4.mp4](../../build/first-trailer-finishing-d4/first-trailer-finishing-d4.mp4). D4 adds audio-driven lip sync for all twenty visible dialogue cues, a recorded ukulele sample performance, and polished stereo location sound/foley. Dan's five large close-ups receive a higher-detail performance refinement. The accepted voices, subtitles, original Fielder reaction and all forty composition durations are preserved.

See [D4 handoff](finishing-d4/README.md), [rendered QC](../../build/first-trailer-finishing-d4/QC.md), and the updated score under build/first-trailer-finishing-d4/score/. This pass used 137 Runway credits; 1,153 remain. The local lip-sync model and its derived drivers are licensed for personal/research/noncommercial use. Some generated mouth/hand details remain approximate.

## D5 ukulele-derived music alternate

A complete alternate score now derives every musical layer from the recorded ukulele sample library: clean performance, displaced plucks, lowered pulse, stretched resonance, distorted clusters, body percussion and reversed plucks. D4 picture, dialogue and clean Roy performance are preserved. No paid generations were used. The D4 cut remains the comparison. See `ukulele-d5/README.md` for the editable score, MIDI, event map, ten audio stems, local renderer and verified 180-second alternate at `build/first-trailer-ukulele-d5/first-trailer-ukulele-d5.mp4`.

## D6 user-notes revision

Completed 3:11 cut with audible opening strums, both original Dan lines, six silent-mouth corrections, photographed Pinterest documents and escalating YOU CAN SEE cards. Forty original holds are retained; four cards add eleven seconds. Score, MIDI, captions and ten stems are retimed together. D4 and D5 are preserved. See `revision-d6/README.md` and `build/first-trailer-revision-d6/first-trailer-revision-d6.mp4`.
