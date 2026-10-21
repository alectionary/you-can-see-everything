\version "2.24.3"
#(set-global-staff-size 15)
\header { title = "YOU CAN SEE EVERYTHING" subtitle = "D5 - a score made entirely from ukulele recordings" subsubtitle = "180 seconds | quarter = 60 | sounding studio pitches" composer = "Original trailer arrangement" tagline = ##f }
\paper { #(set-paper-size "a3") indent = 39\mm short-indent = 14\mm top-margin = 12\mm bottom-margin = 12\mm system-system-spacing.basic-distance = #25 }
global = { \numericTimeSignature \time 4/4 \tempo 4 = 60 \key a \minor
\mark \markup \small "0:00 Roy alone" s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\break s4 s4 \mark \markup \small "0:18 Rehearsal" s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\pageBreak s4 s4 s4 s4 |
s4 s4 s4 s4 |
\mark \markup \small "0:40 Casting" s4 s4 s4 s4 |
s4 s4 s4 s4 |
\break s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 \mark \markup \small "1:02 Corporate review" s4 s4 |
\pageBreak s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\break s4 s4 \mark \markup \small "1:22 Publicity" s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\pageBreak s4 s4 s4 s4 |
s4 s4 s4 s4 |
\mark \markup \small "1:44 Stream intro" s4 s4 s4 s4 |
s4 s4 \mark \markup \small "1:50 Roy plays" s4 s4 |
\break s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 \mark \markup \small "2:06 Authenticity" s4 s4 |
\pageBreak s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\break s4 s4 s4 s4 |
\mark \markup \small "2:28 Fracture" s4 s4 s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
\pageBreak s4 s4 s4 s4 |
\mark \markup \small "2:44 Silence / title at 2:46" s4 s4 s4 s4 |
s4 s4 \mark \markup \small "2:50 Room only" s4 s4 |
s4 s4 s4 s4 |
s4 s4 s4 s4 |
 }
royMusic = \absolute { r4 <a>8\p~ <a>16 r16 <e'>8~ <e'>16 r16 <cis'>8~ <cis'>16 r16 |
 r1 |
 r1 |
 <a>8~ <a>16 r16 <e'>8~ <e'>16 r16 <c'>8~ <c'>16 r16 <e'>8~ <e'>16 r16 |
 <a>8~ <a>16 r16 <e'>8~ <e'>16 r2 r16 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r2 <a>8~ <a>16 r16 <e'>8~ <e'>16 r16 |
 <c'>8~ <c'>16 r16 <e'>8~ <e'>16 r16 <a>8~ <a>16 r16 <e'>8~ <e'>16 r16 |
 <c'>8~ <c'>16 r16 <e'>8~ <e'>16 r16 <a>8~ <a>16 r16 <e'>8~ <e'>16 r16 |
 <c'>8~ <c'>16 r16 <e'>8~ <e'>16 r16 <a>8~ <a>16 r16 <e'>8~ <e'>16 r16 |
 <c'>8~ <c'>16 r16 <e'>8~ <e'>16 r2 r16 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 }
plucksMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r2 <a>8\pp r4 <e'>8 |
 r4 <c'>8 r2 r8 |
 r2 <a>8\p r4 <e'>8 |
 r4 <c'>8 r2 r8 |
 r2 <a>8 r4 <e'>8 |
 r4 <c'>8 r2 r8 |
 r2 <a>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <a>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <a>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r1 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r1 |
 r2 <ees a bes>8\mf r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r2 r8 |
 r2 <ees a bes>8 r4 <e'>8 |
 r4 <c' cis'>8 r8 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 |
 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 |
 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 |
 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 <a bes fis'>16 r16 <bes b fis'>16 r16 <b c' fis'>16 r16 <c' cis' fis'>16 r16 |
 r2 <a,, a, a bes b c' ees' e' fis'>2\ff~ |
 <a,, a, a bes b c' ees' e' fis'>2 r2 |
 r1 |
 r1 |
 }
lowMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 <a,,>8\pp~ <a,,>16 r2 r4 r16 |
 <a,,>8~ <a,,>16 r2 r4 r16 |
 <a,,>8~ <a,,>16 r2 r4 r16 |
 <a,,>8~ <a,,>16 r2 r4 r16 |
 <a,,>8\p~ <a,,>16 r2 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <e,,>8\mf~ <e,,>16 r4 r16 <e,,>8~ <e,,>16 r4 r16 |
 <bes,,>8~ <bes,,>16 r4 r16 <bes,,>8~ <bes,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <a,,>8~ <a,,>16 r4 r16 <a,,>8~ <a,,>16 r4 r16 |
 <e,,>8~ <e,,>16 r4 r16 <e,,>8~ <e,,>16 r4 r16 |
 <bes,,>8~ <bes,,>16 r16 <bes,,>8~ <bes,,>16 r16 <bes,,>8~ <bes,,>16 r16 <bes,,>8~ <bes,,>16 r16 |
 <a,,>8~ <a,,>16 r8 r16 <a,,>8~ <a,,>16 r16 <e,,>8~ <e,,>16 r16 <bes,,>8~ |
 <bes,,>16 r16 <a,,>8~ <a,,>16 r16 <a,,>8~ <a,,>16 r16 <e,,>8~ <e,,>16 r16 <bes,,>8~ |
 <bes,,>16 r16 <a,,>8~ <a,,>16 r16 <a,,>8~ <a,,>16 r16 <e,,>8~ <e,,>16 r16 <bes,,>8~ |
 <bes,,>16 r16 <a,,>8~ <a,,>16 r16 <a,,>8~ <a,,>16 r16 <e,,>8~ <e,,>16 r16 <bes,,>8~ |
 <bes,,>16 r16 <a,,>8~ <a,,>16 r8 r16 <a,,>8\f <a,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 |
 <a,,>8\f <bes,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 |
 <e,,>8\f <bes,,>16\mf r16 <e,,>8\f <a,,>16\mf r16 <e,,>8\f <a,,>16\mf r16 <e,,>8\f <a,,>16\mf r16 |
 <bes,,>8\f <bes,,>16\mf r16 <bes,,>8\f <a,,>16\mf r16 <bes,,>8\f <a,,>16\mf r16 <bes,,>8\f <a,,>16\mf r16 |
 <a,,>8\f <bes,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 <a,,>8\f <a,,>16\mf r16 |
 <a,,>8\f <bes,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 |
 <e,,>8\ff <bes,,>16\mf r16 <e,,>8\ff <a,,>16\mf r16 <e,,>8\ff <a,,>16\mf r16 <e,,>8\ff <a,,>16\mf r16 |
 <bes,,>8\ff <bes,,>16\mf r16 <bes,,>8\ff <a,,>16\mf r16 <bes,,>8\ff <a,,>16\mf r16 <bes,,>8\ff <a,,>16\mf r16 |
 <a,,>8\ff <bes,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 |
 <a,,>8\ff <bes,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 <a,,>8\ff <a,,>16\mf r16 |
 r2 <a,,>2\ff~ |
 <a,,>2 r2 |
 r1 |
 r1 |
 }
bloomMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r2 <a c' e'>2\pp~ |
 <a c' e'>2 <a c' e'>2~ |
 <a c' e'>2 <a c' e'>2~ |
 <a c' e'>2 <a c' e'>2~ |
 <a c' e'>2 <a c' e'>2~ |
 <a c' e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2\p~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2\mf~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes e'>2~ |
 <a bes e'>2 <a bes ees' e'>2~ |
 <a bes ees' e'>2 <a bes ees' e'>2~ |
 <a bes ees' e'>2 <a bes ees' e'>2~ |
 <a bes ees' e'>2 <a bes ees' e'>2~ |
 <a bes ees' e'>2 <a bes ees' e'>2\f~ |
 <a bes ees' e'>2 <a bes ees' e'>2~ |
 <a bes ees' e'>2 <a bes b e' fis'>2~ |
 <a bes b e' fis'>2 <a bes b e' fis'>2~ |
 <a bes b e' fis'>2 <a bes b e' fis'>2~ |
 <a bes b e' fis'>2 <a bes b e' fis'>2 |
 r2 <a bes ees' e' f' fis'>2\ff~ |
 <a bes ees' e' f' fis'>2 r2 |
 r1 |
 r1 |
 }
gritMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 <a,, ees, bes,>4\f~ <a,, ees, bes,>8 r8 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 |
 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 |
 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 |
 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 <a,, ees, bes,>4~ <a,, ees, bes,>8 r8 |
 r2 <a,, ees, bes,>2\ff~ |
 <a,, ees, bes,>2 r2 |
 r1 |
 r1 |
 }
bodyMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r2 c'16\pp r4 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 r4 \once \override NoteHead.style = #'cross c'16 r4 r16 c'16 r4 r16 |
 \once \override NoteHead.style = #'cross c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 c'16 r8 r16 |
 r8 \once \override NoteHead.style = #'cross c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 c'16 r16 |
 r4 \once \override NoteHead.style = #'cross c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 |
 c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r8 r16 |
 r8 c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 r4 c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r4 r16 |
 \once \override NoteHead.style = #'cross c'16 r4 r16 c'16 r4 r16 \once \override NoteHead.style = #'cross c'16 r8 r16 |
 r8 \once \override NoteHead.style = #'cross c'16 r4 r16 c'16\p r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 |
 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 |
 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 \once \override NoteHead.style = #'cross c'16\mf r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 |
 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 |
 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 \once \override NoteHead.style = #'cross c'16 r16 c'16 r16 |
 r1 |
 r1 |
 r1 |
 r1 |
 }
reverseMusic = \absolute { r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r2 r8 r16 <e'>4\p~ <e'>16 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r8 r16 <c'>4~ <c'>16 r2 |
 r1 |
 r1 |
 r1 |
 r1 |
 r8 <a>4~ <a>8 r2 |
 r1 |
 r1 |
 r1 |
 r4 <e'>4 r2 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r1 |
 r8 <e'>4\mf~ <e'>8 r2 |
 r1 |
 r1 |
 r1 |
 r1 |
 r2 <c'>2 |
 r1 |
 r1 |
 r2 r8 <a>4~ <a>8 |
 r2 r8 <bes>4~ <bes>8 |
 r1 |
 r1 |
 r1 |
 r1 |
 }
\markup \column { \small "A-E-C-E passes from Roy to displaced plucks, stretched resonance and low pulses. Each 4/4 bar lasts four seconds." \small "Low pitches, sustains, reversal and distortion are sample processing; these are not solo-instrument fingerings." \small "Body staff: round note = body tap; cross note = muted strum. MIDI is timing interchange, not the finished timbre." \small "Roy retains D4 microtiming; all other onsets follow this grid. Silence at 2:44; one attack at 2:46; no music after 2:50." }
\score { <<
\new Staff \with { instrumentName = "Roy - clean ukulele" shortInstrumentName = "Roy" } << \global { \clef treble \royMusic } >>
\new Staff \with { instrumentName = "Uke - displaced motif" shortInstrumentName = "Pluck" } << \global { \clef treble \plucksMusic } >>
\new Staff \with { instrumentName = "Uke - lowered pulse" shortInstrumentName = "Low" } << \global { \clef bass \lowMusic } >>
\new Staff \with { instrumentName = "Uke - stretched resonance" shortInstrumentName = "Bloom" } << \global { \clef treble \bloomMusic } >>
\new Staff \with { instrumentName = "Uke - distorted cluster" shortInstrumentName = "Grit" } << \global { \clef bass \gritMusic } >>
\new Staff \with { instrumentName = "Uke - body / muted strum" shortInstrumentName = "Body" \override StaffSymbol.line-count = #1 } << \global { \clef percussion \bodyMusic } >>
\new Staff \with { instrumentName = "Uke - reversed breath" shortInstrumentName = "Rev." } << \global { \clef treble \reverseMusic } >>
>> \layout { \context { \Score \override RehearsalMark.self-alignment-X = #LEFT } } }
