# Music and sound cues

Revised Oct 18, 2026 to describe the score as delivered from v6 onward, per Daniel's direction (audible dramatic notes). The original "almost nothing" design below it in git history is superseded. Mix built at 48kHz PCM; final delivery AAC 192k. Dialogue stays dry and centered.

Design: near-silence and room tone as the baseline; a sparse mid-register piano motif (fundamentals 110–220Hz with full harmonics, so the notes survive phone speakers) placed only on dramatic beats; a low swell under the final stare that cuts to true silence for the black frame; one deep title note.

| Cue | Master entry | Content | Envelope / gain |
|---|---|---|---|
| R1 room tone | 0.000–55.000 | Seeded white noise, bandpass 100–3000Hz | Sustain; hard cut at 55.000; −48dB |
| H1 electrical hum | 0.000–55.000 | 60Hz sine | Sustain; hard cut at 55.000; −66dB |
| D1 low drone | 18.000–40.000 | 43.65Hz sine (F1) | 6s raised-cosine attack/release; −42dB |
| N1 piano note | 11.000 | A3 220Hz | 0.008s attack, exp decay τ=1.5s; −15dB |
| N2 piano note | 27.200 | E3 164.81Hz (rings out of Roy's line) | τ=1.5s; −15dB |
| N3 piano note | 34.600 | C3 130.81Hz (pause inside the deceive-you exchange) | τ=1.3s; −16dB |
| N4 piano note | 40.000 | A2 110Hz (under the reaction shot's tail) | τ=1.4s; −16dB |
| SWELL pad | 42.000–55.000 | A-minor pad (110 / 164.81 / 220 / 261.63Hz), lowpass 1200Hz | 3s attack, sustain, hard cut at 55.000; −24dB |
| S1 silence | 55.000–56.000 | Digital silence over the black frame | −∞dB |
| T1 title note | 56.000 | A2+A3 struck together | τ=1.8s decay into the end; −13dB |

Piano synthesis: additive sine partials at f, 2f, 3f, 4f, 5f with relative amplitudes 1, 0.5, 0.3, 0.18, 0.1, normalized; attack rises linearly in 0.008s; decay exp(−(t−0.008)/τ); final 0.15s ramps to zero. No reverb. Dialogue pauses are never gated or filled.
