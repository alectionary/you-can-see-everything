# v9 revision build notes (Oct 18, 2026)
Picture: build/v9/video_raw.mp4 concats all v8 segments unchanged except the tail:
card8 rebuilt at 1.5s (same drawtext params as v8, d=1.5), blk05 = 0.5s black,
title = v7 title recipe (LiberationSans-Regular 64, 0xE6E4DF) with text
"YOU CAN SEE EVERYTHING", 4s. Concat order ends: ... grid16 card8 blk05 title.
Audio: build/v9/audio_mix.wav = v8 mix recipe, but the pre-55 piece gets
afade=t=out:st=54.90:d=0.10 before the gate concat (softens the tremolo cliff;
55-56 remains exact zeros from the null segment). NOTE: afade on a full-length
stem silences everything after the fade - apply it only to the trimmed piece.
Score: score.ly header title changed to YOU CAN SEE EVERYTHING; recompiled
(PDF/MIDI regenerated, music identical).
