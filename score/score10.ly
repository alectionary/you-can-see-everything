\version "2.24.3"

\header {
  title = "YOU CAN SEE EVERYTHING"
  subtitle = "V10 — seventy-six seconds under dialogue"
  composer = "Original teaser score"
  tagline = ##f
}

% CLOCK: quarter = 60 throughout; one quarter is exactly one second.
% Bars 1–3: 3 x 4/4 = 12s; b4: 2/4 = 2s (14s).
% Bars 5–8: 4 x 4/4 = 16s (30s).
% Bars 9–11: 3 x 4/4 = 12s (42s).
% D: 42–65 (original 13q + 10q extension); E: 65–67 (2q rest).
% F: 67–76 (9q single title attack). Total: 76 quarter notes.
% Absolute digital silence requires external gating of ALL buses at 65–67.
% Title envelope tau ~1.2s, trimmed exactly at 76; no synth audio rendered here.

global = {
  \numericTimeSignature
  \key a \minor
  \tempo 4 = 60
  % A: 0–14 — leave both opening dialogue windows entirely unarticulated.
  \time 4/4
  \mark \markup "0:00 — almost nothing"
  s1 | s1 | s1 |
  \time 2/4 s2 |
  % B: 14–30 — the same shape, gradually contaminated.
  \time 4/4
  \mark \markup "0:14 — small wrongness"
  s1 | s1 | s1 | s1 |
  % C: 30–42 — deceive-you exchange, unstable harmony.
  \mark \markup "0:30 — the assurance fractures"
  s1 | s1 | s1 |
  % D: 42–65 — stare, density and dynamic ceiling rise.
  \mark \markup "0:42 — beauty curdles"
  s1 | s1 | s1 |
  \time 1/4 s4 |
  % D extension: 55–65, 4 + 4 + 2 quarters.
  \time 4/4 s1 | s1 |
  \time 2/4 s2 |
  % E: 65–67, absolute silence.
  \mark \markup "1:05 — DIGITAL SILENCE"
  s2 |
  % F: 67–76 — one collective attack; no further strikes.
  \time 4/4
  \mark \markup "1:07 — title / decay to 1:16"
  s1 | s1 | \time 1/4 s4 \bar "|."
}

pianoRH = \fixed c' {
  % 0–14: A minor; attacks at 0, 5 and 11 only. No pedal across speech.
  a4\pp r2. | r4 e'4 r2 | r2. c'4 | r2 |
  % 14–30: A–E–C cell, then B-flat, then E-flat. Quiet figure under speech.
  r2. a8\p e'8 | r2 c'4 r4 |
  r4 a8 e'8 r2 | r4 <bes c'>8\< e'8 r4 <a ees'>4\! |
  % 30–42: seconds/tritones; leave 32–34.5 almost empty.
  <a bes e'>4\mf r2. |
  r2 <bes b e'>8 r8 r4 |
  r2 <a bes dis' e'>2 |
  % 42–46: restrained sustained cluster under the last two lines.
  <a bes b e'>1\f |
  % 46–50: delayed attack at 47, then asymmetrical 5:4 grouping.
  r4 <a bes b c' fis'>4\<
  \tuplet 5/4 { <a bes>8 <b c'>8 <ees' e'>8 <fis' g'>8 <a' bes'>8 } |
  % 50–54: seven equal pulses over two beats, then a falling smear.
  \tuplet 7/4 { <b c' fis'>8\ff <c' des' g'>8 <des' d' aes'>8
    <d' ees' a'>8 <ees' e' bes'>8 <e' f' b'>8 <f' ges' c''>8 }
  <fis' g' c'' des''>4\glissando <a bes b c'>4 |
  % 54–55: short tremolo; all keys released at the boundary.
  <a bes b c' dis' e'>4:32\ff |
  % Extended D follows; no pedal across the ensuing silence.
  % V10 D extension: 55–65, increasingly dense, metered.
  \tuplet 5/4 { <a bes b>8\ff <b c' fis'>8 <ees' e'>8 <fis' g'>8 <a' bes'>8 }
  <a bes b c' dis' e'>2:32 |
  \tuplet 7/4 { <b c' fis'>8 <c' des' g'>8 <des' d' aes'>8 <d' ees' a'>8 <ees' e' bes'>8 <e' f' b'>8 <f' ges' c''>8 }
  <fis' g' c'' des''>2:32 |
  <a bes b c' dis' e' fis'>2:32\ff |
  % 65–67: all-staff rest.
  r2 |
  % 67–76: a single massive sonority. Let the mix envelope decay it.
  <a bes b c' dis' e' fis'>1~\fff^\markup { "one attack; decay, no re-strike" } | <a bes b c' dis' e' fis'>1~ | <a bes b c' dis' e' fis'>4 |
}

pianoLH = \fixed c' {
  \clef bass
  R1*3 | R2 |
  % 14–30: bass is still largely absent.
  R1 | r2 a,2\pp | R1 | r2 <ees, a,>2\p |
  % 30–42: widely spaced bass tritones keep the voice band open.
  <a,, ees,>2\mf r2 | R1 | r2 <bes,, e,>2 |
  % 42–55: low foundations accumulate, pulse unmoors.
  <a,, ees,>1\f | <bes,, e,>1\< |
  \tuplet 3/2 { <a,, bes,,>4\ff <ees, e,>4 <a, bes,>4 }
  <a,, ees, bes,>2 |
  <a,, bes,, e,>4:32 |
  % V10 D extension: 55–65.
  <a,, bes,, e,>1:32\ff |
  \tuplet 3/2 { <a,, bes,,>4 <ees, e,>4 <a, bes,>4 } <a,, ees, bes,>2 |
  <a,, bes,, ees, e,>2:32 |
  % 65–67: all-staff rest.
  r2 |
  <a,, bes,, ees, e,>1~\fff | <a,, bes,, ees, e,>1~ | <a,, bes,, ees, e,>4 |
}

strings = \fixed c' {
  % One ensemble staff: divisi chords, GM string ensemble 1.
  R1*3 | R2 |
  % Enters at 16s: consonance is initially still credible.
  r2 <a e' c''>2\pp | <a e' c''>1 |
  <a bes e'>1\p | <a bes ees'>1\< |
  % 30–42: slow semitone grinding, tremolo only in the held tail.
  <a bes dis'>1\mf | <gis a d'>1 | <a bes e' f'>1:16 |
  % 42–55: bowed tremolo becomes the continuous pressure.
  <a bes dis' e'>1:32\f |
  <bes b e' f'>1:32\< |
  <b c' f' fis'>2:32\ff <c' des' fis' g'>2:32 |
  <cis' d' g' aes'>4:32 |
  % V10 D extension: 55–65.
  <b c' f' fis'>1:32\ff |
  <c' des' fis' g'>2:32 <cis' d' g' aes'>2:32 |
  <d' ees' aes' a'>2:32 |
  % 65–67: all-staff rest.
  r2 |
  % No tremolo on the title: one sustained attack, externally decayed.
  <a bes dis' e' f' fis'>1~\fff | <a bes dis' e' f' fis'>1~ | <a bes dis' e' f' fis'>4 |
}

brass = \fixed c' {
  \clef bass
  R1*3 | R2 |
  R1*4 |
  R1*3 |
  % Late entrance at 48s; no brass attacks underneath final answer.
  R1 | r2 <bes,, e,>2\f\< |
  <b,, f,>2\ff <c, fis,>2 |
  <cis, g,>4 |
  % V10 D extension: 55–65.
  <cis, g,>1\ff | <d, aes,>2 <ees, a,>2 |
  <e, bes,>2 |
  % 65–67: all-staff rest.
  r2 |
  <a,, ees, bes,>1~\fff | <a,, ees, bes,>1~ | <a,, ees, bes,>4 |
}


% Programmatic duration assertions (whole-note moments = quarter count / 4).
#(let ((actual (ly:music-length global)))
   (if (not (equal? actual (ly:make-moment 76 4)))
       (ly:error "global: expected 76 quarters, got ~a" actual))
   (display "AUDIT global: 76.000 quarter notes PASS\n"))
#(let ((actual (ly:music-length pianoRH)))
   (if (not (equal? actual (ly:make-moment 76 4)))
       (ly:error "pianoRH: expected 76 quarters, got ~a" actual))
   (display "AUDIT pianoRH: 76.000 quarter notes PASS\n"))
#(let ((actual (ly:music-length pianoLH)))
   (if (not (equal? actual (ly:make-moment 76 4)))
       (ly:error "pianoLH: expected 76 quarters, got ~a" actual))
   (display "AUDIT pianoLH: 76.000 quarter notes PASS\n"))
#(let ((actual (ly:music-length strings)))
   (if (not (equal? actual (ly:make-moment 76 4)))
       (ly:error "strings: expected 76 quarters, got ~a" actual))
   (display "AUDIT strings: 76.000 quarter notes PASS\n"))
#(let ((actual (ly:music-length brass)))
   (if (not (equal? actual (ly:make-moment 76 4)))
       (ly:error "brass: expected 76 quarters, got ~a" actual))
   (display "AUDIT brass: 76.000 quarter notes PASS\n"))

\paper { #(set-paper-size "a3") }
\score {
  <<
    \new PianoStaff \with { instrumentName = "Piano" shortInstrumentName = "Pno." } <<
      \new Staff \with { midiInstrument = "acoustic grand" }
        << \global \pianoRH >>
      \new Staff \with { midiInstrument = "acoustic grand" }
        << \global \pianoLH >>
    >>
    \new Staff \with {
      instrumentName = "Strings (div.)" shortInstrumentName = "Str."
      midiInstrument = "string ensemble 1"
    } << \global \strings >>
    \new Staff \with {
      instrumentName = "Trombones (div.)" shortInstrumentName = "Tbn."
      midiInstrument = "trombone"
    } << \global \brass >>
  >>
  \layout { }
  \midi { \tempo 4 = 60 }
}
