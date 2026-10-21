# First full trailer music and sound cues

Draft 1. Compose for the 180-second timeline in EDIT_PLAN.md. Preserve the teaser’s sparse A-minor piano character, dissonant contamination and collective title attack, while introducing Roy’s original ukulele phrase and an increasingly physical bass rhythm. An editable scratch score, PDF, MIDI and individual stems are now rendered under build/first-trailer-animatic/. The plucked timbre is a nylon-guitar stand-in; the final ukulele performance and production mix remain to be made.

## The phrase that changes ownership

Proposed new four-beat phrase at quarter note = 60: A3, E4, C4, E4, one quarter note each, over a quiet A-minor ukulele voicing. This is a newly proposed composition; it is not an assertion about Roy’s historical song. A close answer to the phrase may descend C4–B3–A3 with a held final note. Keep it simple enough to recognize through reharmonization.

The opening N01 performance has an ordinary missed chord, breath and restart. The pianist adopts its A–E–C outline at 18 seconds. At 104 seconds the clean ukulele phrase returns. During the Pinterest reveal, introduce bass changes approximately one eighth note before Roy’s changes; keep the picture and ukulele audio synchronized. This is an arrangement choice that suggests anticipation, not proof of Dan’s authorship.

Record or synthesize a convincing plucked instrument with believable attack, decay and fingering. GeneralUser GS may support a temporary acoustic-guitar timbre; it is not a verified ukulele instrument and should not be labeled a final ukulele performance. The final phrase needs a suitable instrument source or a played recording.

## Cue sheet

| Cue | Window | Music | Sound and dramatic purpose |
|---|---|---|---|
| M01 | 0–18 | Roy alone; fragile phrase and restart, no non-diegetic score | Modest room noise, instrument handling, breath. Keep Roy a person before he becomes an image inside another image. |
| M02 | 18–40 | Sparse piano answers the phrase; isolated dissonance enters after the first Again | Keep most space around speech. The repeat is exposed by performance and room sound. |
| M03 | 40–62 | Add B-flat/E-flat contamination and a quiet sustained bass; quarter-note pulse emerges gradually | Audition reset sounds and chair movement remain ordinary, not comic stings. |
| M04 | 62–82 | Bass becomes audible, piano increasingly incomplete; thin strings sustain seconds | Corporate screen sounds minimal; let the food-bank environment be audible beneath the narration. |
| M05 | 82–104 | Mechanism rhythm enters the musical arrangement after shredding begins | First establish the real shred sound. Transfer its irregular rattle into percussion without cutting the picture faster. |
| M06 | 104–126 | Roy’s phrase returns exposed, then bass anticipates the harmonic changes | Stream playback stays continuous through T24. Gradually change room perspective as the camera reveals the screen; avoid an instantaneous unexplained audio switch. |
| M07 | 126–148 | Pulse gains eighth-note subdivisions; strings tremolo; low piano retains fragments of the original phrase | The actor’s ukulele has handling noise only. Do not accidentally create a second musical performance. |
| M08 | 148–164 | Strongest bass, controlled low percussion and brass; clusters crowd the phrase | Let L29 and L30 remain intelligible. Roy’s unfinished phrase stops at 163.900; the sound gate arrives at 164.000. |
| M09 | 164–166 | Exact silence on every bus | No reverb, synth release, notification, room tone or transition tail. |
| M10 | 166–170 | One ensemble attack, with low bass reinforcement, then decay | No secondary strikes; no score continues into the final room. |
| M11 | 170–180 | No non-diegetic score | Roy’s breath, close room sound, question, and a modest notification at 175.000. Silence after the notification’s decay is allowed to remain ordinary room ambience. |

## Bass and rhythm

Use quarter = 60 as the timing grid; acceleration comes from subdivisions and density rather than a tempo jump. Start with A1 at 55Hz, with a controlled octave at 110Hz for small speakers. Later introduce E1 at about 41.2Hz, B-flat1 at about 58.3Hz and dissonant upper harmonics. Keep the lowest octave controlled so dialogue is not masked. Do not rely on inaudible sub-bass for the effect.

Avoid a generic action-trailer beat. Early pulses should feel like pressure accumulating; later subdivisions can suggest the shred mechanism continuing after the event. The image holds remain at least two seconds even when the sound is rhythmically dense.

## Notation and delivery plan

Write a new standalone score for this trailer in its own directory after the animatic timing is established. Keep score/score10.ly and its MIDI/PDF unchanged. Notate piano, plucked instrument, bass, strings, brass and a percussion/rhythm staff; indicate sound-design transfers explicitly. Quarter=60 makes the initial timeline 180 quarter notes. A future longer hold extends all applicable bars and cue windows.

Export independent stems for dialogue, on-screen ukulele, score piano, bass, strings, brass, percussion, ambience and effects. Keep Dan’s two reused recordings unpitched; match new voices to them rather than processing them to fit a new casting choice.

## Mix and verification

Work at 48kHz PCM. At exactly 180 seconds, the mix has 8,640,000 samples per channel. Gate 164.000–166.000 to exact zero on every PCM bus: zero-based samples 7,872,000 through 7,967,999 inclusive. The title attack begins at sample 7,968,000; end its score buses by 170.000. Check all stems as well as the master. AAC can introduce tiny nonzero samples at gate edges; assess the viewing copy separately from the exact PCM test.

Start dialogue-first. Duck bass and dense score during speech while preserving consonants and natural room perspective. A provisional web mix target is about −16 LUFS integrated, true peak no higher than −1dBTP; confirm by listening and measurement rather than forcing the piece to a number. Preserve the opening-to-climax contrast. Check mono compatibility and laptop/phone playback, particularly the 110Hz bass component and ukulele intelligibility.

The musical test is whether we can still recognize a trace of Roy’s tune at the point it feels most appropriated. Its increased scale should make the final unaccompanied question feel exposed.

## D4 rendered performance and mix

The latest full cut uses recorded tenor ukulele samples (FreePats / Mateusz Dąbrowski, CC0), replacing the nylon-guitar proxy. The written phrase is retained with small natural timing/velocity variations. Its middle-section entry is now at 110.000 seconds after the spoken introduction; bass remains half a beat ahead. Instrument filtering and pan change gradually through the screen pullback. The initial wrong C-sharp, restart and larger score structure are preserved.

D4 adds restrained location beds and practical shred, clap and handling sounds. The stereo master targets approximately −18 LUFS and preserves the 164–166 exact-zero PCM gate, single title attack and music-free last ten seconds. See finishing-d4/README.md, the updated score under build/first-trailer-finishing-d4/score/, and the measured rendered QC report.

## D5 single-source musical alternate

The D5 arrangement retains the D4 note/timing map while revoicing the non-diegetic score exclusively with saved ukulele recordings. The old piano line becomes displaced plucks, bass becomes lowered recorded notes, strings become stretched ringing notes, brass becomes filtered/saturated low chords, and mechanism percussion becomes instrument body taps and muted strums. Eight short reversed plucks arrive at structural turns. Roy remains byte-identical to D4; the bass anticipation, exact 164-166 silence, single title attack and music-free last ten seconds remain. Sheet music displays sounding studio pitches and is not a playable solo-ukulele transcription. See `ukulele-d5/README.md` and `build/first-trailer-ukulele-d5/score/`. D4 remains intact for listening comparison.

## D6 extended score and clear opening strums

Runtime is now 191 seconds. New cards at 79-81, 106-108 and 168-171 have newly extended or written musical events. Opening single-note material becomes clearly ringing four-string ukulele strums (5.49 dB higher instrument RMS); the clean middle performance is retained at 114-130, with bass anticipation at 113.5. Exact silence is 171-173, one title attack at 173, music ends at 177, and the final CTA at 187-191 remains silent. No original picture hold or voice is shortened. See `revision-d6/README.md` for the updated written score, MIDI, event map, stems and rendered QC.
