# D5 ukulele-derived alternate - rendered QC

Technical verification passed on the delivered MP4, MIDI, score and PCM stems. This is an alternate score for the accepted D4 picture, not a new picture edit.

180.000 seconds, 4320 frames, 1280 x 720, 24 fps, stereo 48 kHz AAC. Encoded loudness -18.05 LUFS; true peak -1.53 dBTP; range 12.30 LU. Mono fold-down change -0.0111 dB. Encoded gap peak -79.77 dBFS.

## RULES.md audit

Every picture segment is unchanged. The H.264 elementary-stream hash matches D4 exactly, so every pixel and edit boundary inherits the verified D4 picture. No interval was shortened and no extra cut was introduced. Minimum segment duration is 2.000 seconds. Dialogue stem and caption bytes are identical to D4; Roy, effects and ambience stems are also byte-identical before common master gain.

| Segment | Start | End | Duration | Frames | Minimum | Result |
|---|---:|---:|---:|---:|---:|---|
| T01 | 0.000 | 8.000 | 8.000 | 192 | 2.000 | PASS |
| T02 | 8.000 | 12.000 | 4.000 | 96 | 2.000 | PASS |
| T03 | 12.000 | 18.000 | 6.000 | 144 | 2.000 | PASS |
| T04 | 18.000 | 22.000 | 4.000 | 96 | 2.000 | PASS |
| T05 | 22.000 | 26.000 | 4.000 | 96 | 2.000 | PASS |
| T06 | 26.000 | 30.000 | 4.000 | 96 | 2.000 | PASS |
| T07 | 30.000 | 34.000 | 4.000 | 96 | 2.000 | PASS |
| T08 | 34.000 | 37.000 | 3.000 | 72 | 2.000 | PASS |
| T09 | 37.000 | 40.000 | 3.000 | 72 | 2.000 | PASS |
| T10 | 40.000 | 48.000 | 8.000 | 192 | 2.000 | PASS |
| T11 | 48.000 | 52.000 | 4.000 | 96 | 2.000 | PASS |
| T12 | 52.000 | 56.000 | 4.000 | 96 | 2.000 | PASS |
| T13 | 56.000 | 62.000 | 6.000 | 144 | 2.000 | PASS |
| T14 | 62.000 | 67.000 | 5.000 | 120 | 2.000 | PASS |
| T15 | 67.000 | 72.000 | 5.000 | 120 | 2.000 | PASS |
| T16 | 72.000 | 76.000 | 4.000 | 96 | 2.000 | PASS |
| T17 | 76.000 | 79.000 | 3.000 | 72 | 2.000 | PASS |
| T18 | 79.000 | 82.000 | 3.000 | 72 | 2.000 | PASS |
| T19 | 82.000 | 88.000 | 6.000 | 144 | 2.000 | PASS |
| T20 | 88.000 | 94.000 | 6.000 | 144 | 2.000 | PASS |
| T21 | 94.000 | 98.000 | 4.000 | 96 | 2.000 | PASS |
| T22 | 98.000 | 104.000 | 6.000 | 144 | 2.000 | PASS |
| T23 | 104.000 | 110.000 | 6.000 | 144 | 2.000 | PASS |
| T24 | 110.000 | 118.000 | 8.000 | 192 | 2.000 | PASS |
| T25 | 118.000 | 122.000 | 4.000 | 96 | 2.000 | PASS |
| T26 | 122.000 | 126.000 | 4.000 | 96 | 2.000 | PASS |
| T27 | 126.000 | 132.000 | 6.000 | 144 | 2.000 | PASS |
| T28 | 132.000 | 138.000 | 6.000 | 144 | 2.000 | PASS |
| T29 | 138.000 | 142.000 | 4.000 | 96 | 2.000 | PASS |
| T30 | 142.000 | 145.000 | 3.000 | 72 | 2.000 | PASS |
| T31 | 145.000 | 148.000 | 3.000 | 72 | 2.000 | PASS |
| T32 | 148.000 | 151.000 | 3.000 | 72 | 2.000 | PASS |
| T33 | 151.000 | 154.000 | 3.000 | 72 | 2.000 | PASS |
| T34 | 154.000 | 157.000 | 3.000 | 72 | 2.000 | PASS |
| T35 | 157.000 | 160.000 | 3.000 | 72 | 2.000 | PASS |
| T36 | 160.000 | 164.000 | 4.000 | 96 | 2.000 | PASS |
| T37 | 164.000 | 166.000 | 2.000 | 48 | 2.000 | PASS |
| T38 | 166.000 | 170.000 | 4.000 | 96 | 2.000 | PASS |
| T39 | 170.000 | 175.000 | 5.000 | 120 | 2.000 | PASS |
| T40 | 175.000 | 180.000 | 5.000 | 120 | 2.000 | PASS |

## Score and sound

All 10 stereo 24-bit stems and the master have exactly 8,640,000 frames. Every bus is exactly zero from 164 to 166. Music is exactly zero after 170. The shared title attack is at 166; there are no later note events. The bass retains its 109.5-second start and half-beat anticipation. Roy retains the original microtiming and screen-perspective treatment. The three opening pitches were measured on the decoded delivery MP4; the lowered A1 was measured on the actual rendered low stem. All four are within 15 cents.

The delivered eight-track MIDI was parsed and its note onsets, durations, velocities, tempo and length checked against the arrangement event map. The six-page LilyPond production score compiles without warnings. All pages were rendered to PNG and checked for layout. These are sounding studio pitches and processing instructions; some parts intentionally extend beyond a real ukulele's playable range. MIDI is interchange data, not a faithful audio preview of the transformed timbres.

All musical source audio comes from the saved CC0 FreePats Flight Fireball ukulele library. Piano, brass, strings and drum generators are absent from this mix. Practical shred/room/notification effects remain outside the musical score. No credits or paid generations were used.

## Review limits

The checks establish file integrity, timing, pitch, levels, source continuity and layout. They do not assert subjective listening approval. The picture retains its D4 label and approximate generated mouth/hand detail because the video stream was deliberately preserved. D4 remains the comparison cut.
