# D5: ukulele-derived score alternate

This is a completed 180-second musical alternate for the D4 finishing cut. D4 remains intact for comparison. All new musical sounds originate in the recorded Flight Fireball tenor ukulele library already saved under `trailer/first/finishing-d4/samples/ukulele/` (Mateusz Dąbrowski / FreePats, CC0). No paid generations were made.

## Deliverables

- `build/first-trailer-ukulele-d5/first-trailer-ukulele-d5.mp4`: complete alternate trailer, original D4 video stream and captions; the visible D4 picture label is intentionally retained.
- `build/first-trailer-ukulele-d5/mix.wav`: stereo 48 kHz / 24-bit full master.
- `build/first-trailer-ukulele-d5/music-only.wav`: music at pre-master mix balance, without dialogue or practical effects.
- `build/first-trailer-ukulele-d5/audio-review/`: full music-only MP3 and short full-mix excerpts for opening/rehearsal, Pinterest reveal and ending.
- `build/first-trailer-ukulele-d5/score/ukulele-score-d5.pdf`: six-page A3 production score, rendered and visually checked.
- Adjacent `.ly`: editable LilyPond source; `.mid`: eight-track MIDI, including conductor/tempo; seven separate role MIDI files; `events.json` and `event-cues.csv`: exact pitch, onset, duration and velocity map.
- `build/first-trailer-ukulele-d5/stems/`: ten stereo 48 kHz / 24-bit WAVs, all 180 seconds: roy, plucks, low, bloom, grit, body, reverse, dialogue, effects, ambience.
- `QC.json` and `QC.md`: rendered artifact measurements and explicit audit of all 40 picture segment durations.

## Workflow and musical intent

1. Retain the accepted D4 event map: quarter note = 60, one quarter per second, four seconds per 4/4 bar. Reuse the A-E-C-E motif, displaced answers, dissonant clusters, original pulse subdivisions and the bass entering half a beat before Roy at 109.5 seconds. The clean performance starts at 110 after Roy's spoken introduction.
2. Revoice the old piano/bass/strings/brass/percussion roles using only recorded ukulele notes, body taps and muted strums. Add eight reversed-pluck breaths that arrive at structural turns. The old synthesized musical stems do not enter this mix.
3. Use one event map for the LilyPond score, MIDI and audio. The score displays sounding studio pitches, including transformed bass pitches outside a real ukulele's range. It is a production arrangement rather than a playable solo-ukulele part. MIDI carries notes/timing only; a generic MIDI player will not recreate the finished processed timbres.
4. Render recorded notes with resampling, phase-vocoder stretching, filtering, soft saturation, short echoes, amplitude modulation and stereo placement. Low pulse retains playable upper harmonics for small speakers. The clean Roy stem is byte-identical to D4. At 110, the other textures briefly recede and gradually return as the screen is revealed.
5. Follow real saved dialogue lengths for smooth score ducking. Match the previous arrangement's broad role balances, then master to approximately -18 LUFS. Preserve exact PCM silence from 164 to 166, one shared title attack at 166, and no music after 170.
6. Copy D4's encoded video stream without re-encoding. Preserve the dialogue, effects and ambience stems before common master gain. Verify actual exported duration, stream identity, sample counts, silence, pitch, levels and MIDI events. Render all six PDF pages for layout review.

## Processing roles

| Role | Material and treatment | Function |
|---|---|---|
| Roy | Accepted D4 ukulele performance, unchanged | Human, intimate source; existing slight microtiming and screen perspective remain |
| Plucks | Recorded notes, subtle detuned doubles, short echoes, gradually stronger soft saturation | Carries the displaced motif formerly assigned to piano |
| Low | Recorded C4 resampled down to A1/E1/B-flat1, low-pass plus parallel saturation | Original ominous pulse and bass anticipation |
| Bloom | Recorded notes stretched at fixed pitch, soft swells, gradually deeper/faster amplitude modulation | Suspended harmony and dissonant pressure formerly assigned to strings |
| Grit | Recorded low chords stretched, filtered and saturated | Late dense, rough chord pressure formerly assigned to brass |
| Body | Real body tap and muted-strum articulations; slight lowering later | Physical pulse, without a synthesized drum |
| Reverse | Backward recorded plucks | Sparse breaths into structural turns; all end by the silence gate |

Published SFZ tuning offsets are applied to transpositions. A3 is derived from C4, as in the accepted D4 Roy performance. The source library and license remain saved in the D4 sample directory.

## Rebuild

Use the existing local environment `/private/tmp/ycs-finishing-venv/bin/python` (dependency lock is `trailer/first/finishing-d4/requirements-lock.txt`), plus FFmpeg and LilyPond. Runtime Python base is the bundled Codex Python 3.12. No neural model, API token, network access or Runway call is needed to reproduce this musical alternate.

```sh
/private/tmp/ycs-finishing-venv/bin/python trailer/first/ukulele-d5/build_ukulele.py compose score audio export
/private/tmp/ycs-finishing-venv/bin/python trailer/first/ukulele-d5/verify_ukulele.py
```

Individual stages can run separately. A temporary environment may eventually disappear; recreate it from the saved dependency lock if necessary. Source samples and delivered outputs are durable repository files. For music edits, modify the event map/processing in the new renderer, not the preserved D4 sources. Re-render and inspect the score PDF after notation edits.

## Comparison and remaining judgment

D4 is the orchestral comparison; D5 is the single-instrument-source alternate. Integrated loudness is close enough for a useful comparison. Technical checks do not establish subjective headphone/speaker approval. The intended listening question is whether the clean ukulele remains emotionally recognizable as its surrounding textures become darker, and whether the climax has enough weight without hiding dialogue.

All D4 picture limits remain, including approximate generated mouths and hand fingering. Its personal/noncommercial performance-model terms also remain attached to the preserved picture. The user's intended use is personal and noncommercial.
