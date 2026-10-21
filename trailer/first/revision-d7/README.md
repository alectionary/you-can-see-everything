# D7 — performance and editorial revision

Delivery: `build/first-trailer-revision-d7/first-trailer-revision-d7.mp4` (3:11).

This pass addresses the user's reports of silent ukulele strokes, exaggerated head motion, fuzzy mouth composites and Roy appearing to speak Dan's signature line. Earlier cuts remain intact.

Dan visibly delivers “I'm engaging with you as a human being” in T35. Its accepted recording moves from 162.2 to 161.3 seconds and ends at 162.993; the caption clears by 163.55, before Roy appears at 164. Dan's identity is reinforced with the lower third “DAN / CEO / Pinterest.” The same stock voice recordings and dialogue wording are retained throughout.

Eight interview compositions use native Runway performances from stationary character images, facial expressiveness 1, gestures off. The final images are the native outputs directly, with no enlarged 96-pixel mouth patch. Each full frame holds after its last spoken word plus about 100 ms, preventing continued mouth movement during the shot tail without blending or masking the lips. Temporary driver mouth renders remain only under `drivers/`; they are not delivery sources.

The user's editorial suggestions become part of the fiction: the Roy auditions appear as sharp contact-sheet audio review sessions; the original Fielder reaction returns in a reaction-selects composition. The interview and communications exchanges use reverse-angle photographs with faces outside the frame. Roy's introductions and final question use instrument coverage. The unfinished Roy line is heard over laptop coverage. These preserve uncertainty about who controls the footage while avoiding distracting face artifacts.

Roy's clean instrument now starts at time zero and continues throughout the opening: ringing chords at 0–8, pitched palm-muted strokes under the apology at 8–12, and the restart at 12–18. Quiet strums cover 108–114. The accepted middle performance at 114–130 remains unchanged. The non-diegetic transformed score still ends at 177, while the dry room ukulele continues until 187, including 2:59 and the Pinterest reply. The CTA at 187–191 is silent. The wrong chord remains, now at the end of the opening phrase. All seven score voices continue to derive from ukulele recordings.

The six-page LilyPond score, MIDI, event map, stems, caption file and final mix live under the D7 build directory. Image prompts and hashes are under `images/provenance.json`; Runway task IDs and settings are under `build/first-trailer-revision-d7/performance/provenance.json`. Three native performance generations used 150 existing Runway credits, including the 4-second test. No new voice generation or subscription purchase was made. The user explicitly approved uploading the fictional character performance clips and stills to the existing Runway workspace.

## Rebuild

Use the existing `/private/tmp/ycs-finishing-venv/bin/python` environment, ffmpeg, LilyPond and Poppler. Preserve the saved native performance outputs; rebuilding does not call paid APIs.

```sh
python trailer/first/revision-d7/build_revision.py prepare compose score audio picture export
python trailer/first/revision-d7/verify_revision.py
```

The picture stage resumes existing segments. To deliberately change a segment's rendering, remove only that D7 derived segment before rebuilding. The driver preparation script is optional provenance and is not needed to rebuild from the saved native outputs.

## RULES.md and review

All 44 D6 picture holds retain their durations; the shortest remains 2.000 seconds. No shot is shortened to fund another. Full-trailer revisions are explicitly authorized; accepted speech PCM and words survive, with only the documented move of L29 to the Dan shot. Cards overlap no spoken-caption window. `QC.md` lists every segment and its actual frame count/duration. `QC.json` records checks on the actual encoded delivery, including half-second audio energy during visible playing, native face-detail comparisons, speech-tail holds, head-motion comparison, source-voice correlations, loudness, pitch, black/silence, MIDI and scene scans.

Technical checks establish sound presence, source selection and encoding behavior. Sampled-frame visual review covers opening, dialogue, audition screens, rear angles, speaker handoff and ending. They do not certify exact generated fingering or perfect phonemes, and subjective headphone/speaker listening approval is not claimed.
