# First trailer finishing cut D4

Delivery: `build/first-trailer-finishing-d4/first-trailer-finishing-d4.mp4`. This is the full 180-second cut with audio-driven dialogue, recorded ukulele sample performance and stereo sound polish. D3 and all earlier versions are preserved. No commits or pushes were made.

## Picture and voices

Twenty visible dialogue cues were driven from their exact accepted recordings. The two characters in the table shot were processed independently. The final Roy question and Pinterest comment use a continuous ten-second source. Two additional silent passes suppress unrelated speaking motion in T31 and T35. The original user-selected Fielder reaction remains untouched in T05; practice-shot mouth changes preserve the original upper-face expressions.

The local Wav2Lip GAN pass runs on Apple MPS, with a narrow feather around the lips and jaw. Dan's five large close-ups receive a second Runway performance-capture refinement, using the local synchronized result as the driving performance and the original Dan footage as the character reference. Those refinements resynthesize facial detail and can vary eye or head movement slightly. Exact prompts, task IDs, hashes and selection notes are in the adjacent provenance files and clips/first/finishing-d4/performance/*.json.

All 31 saved speech PCM files and the accepted caption file are preserved byte for byte. Voices retain their pitch, words and natural duration; the master changes level and perspective rather than retiming speech. The corrected opening question and longer “I was” remain active.

## Ukulele and sound

The guitar placeholder is replaced by a performed sample arrangement of real Flight Fireball tenor ukulele recordings by Mateusz Dąbrowski, published through FreePats under CC0. Samples and their license are in samples/ukulele/. Source: https://freepats.zenvoid.org/GuitarFamily/ukulele.html .

The A–E–C–E motif, initial wrong note and restart remain recognizable. The middle performance starts at 110 seconds after Roy's spoken introduction, keeping the bass half a beat ahead. Small timing and velocity variations and natural sample tails provide the performance. A3 is transposed from the recorded C4 sample by three semitones. At the Pinterest pullback the instrument gradually narrows in frequency range, loses a little level and moves toward the screen at left. The rest of the established score is retained. Hands still come from generated footage; exact string/fret correspondence is approximate.

New sound includes quiet home and lodge beds, a practical canvas-shredder motor and tearing sound, one tentative clap and soft ukulele handling. The original notification remains at 175 seconds. Sound is stereo, 48kHz / 24-bit PCM with an encoded AAC viewing copy. The master targets about −18 LUFS while retaining the original dynamic contrast. Every PCM bus is exactly silent from 164 to 166; the title retains one ensemble attack; all music stops by 170.

The generated music experiment is retained as a comparison source but is not used in the delivered master. The final instrument uses the recorded sample library and our written melody.

## Reproduce and audit

`finish_sound.py` renders the sample performance and mix; `sync_batch.py` performs local audio-driven mouth generation; `refine_mouths.py` restores more original cheek/nose texture; `build_finish.py picture export` assembles the reviewed local and selected Runway sources; `verify_finish.py` measures the final artifact. `build_finish.py score` updates the editable notation and ukulele MIDI. Existing segments are cached; remove only the changed segment before rebuilding.

The current runtime is /private/tmp/ycs-finishing-venv and the official model source is /private/tmp/ycs-wav2lip. requirements-lock.txt and local-model-provenance.json record installed versions, source commit, official download URLs and model hashes for restoration. The local source has one device-guard adaptation to accept Apple MPS; the current librosa mel filter uses keyword arguments. Rebuilding from saved performance videos does not need the neural model or any API call.

All forty compositions retain the approved durations and meet the two-second minimum under RULES.md. No hold was shortened. QC.json and QC.md measure the actual export, its silence and black frames, source continuity, ukulele tuning, stereo/mono behavior, loudness and per-segment frames. Sampled-frame review is saved separately; it is not a claim of human headphone/speaker listening approval or flawless phoneme-level performance.

## Source terms and credits

The local Wav2Lip model is limited to personal/research/noncommercial use: https://github.com/Rudrabha/Wav2Lip . That restriction also applies to its performance drivers and is not removed by subsequent refinement. This delivery is suitable for private noncommercial review; a commercial release needs an appropriately licensed replacement for those passes.

This finishing pass used 137 Runway credits: 37 for six audio sources, 20 for a four-second detail test and 80 for the remaining sixteen seconds of Dan's close-ups. The verified balance is 1,153, above the earlier 510-credit reserve. No purchases or account-plan changes were made. No new ElevenLabs lines were generated in this pass.
