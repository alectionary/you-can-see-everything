# Visual production tests v1

Four continuity keyframes generated with the built-in image_gen tool, plus an authored Pinterest wrapper, a screen-compositing proof and a Fielder reaction reference reel. These are separate from the accepted D2-r1 trailer.

- [Roy → Pinterest → viewing room: 18-second compositing test](../../../../build/first-trailer-visual-tests-v1/roy-pinterest-reveal-test-v1.mp4)
- [Fielder: original motion anchor and new static reference poses](../../../../build/first-trailer-visual-tests-v1/fielder-rehearsal-reference-v1.mp4)
- [Shot prompts and acceptance criteria](SHOT_PROMPTS.md)
- [Structured shot cards](shot-prompts.json)
- [Exact image-generation prompts](image-prompts.json) and [asset provenance](asset-manifest.json)
- [Rendered test QC](../../../../build/first-trailer-visual-tests-v1/QC.md)

## First moving rehearsal test

- [Original versus new take, four seconds each](../../../../build/first-trailer-visual-tests-v1/fielder-motion-test/fielder-original-versus-new-test-01.mp4)
- [Full new take](../../../../build/first-trailer-visual-tests-v1/fielder-motion-test/fielder-rehearsal-test-01.mp4)
- [Motion test QC](../../../../build/first-trailer-visual-tests-v1/fielder-motion-test/QC.md)

Runway generated a distinct 8.041667-second / 193-frame silent clip at 1280×720, 24fps. The planned source 2–6 second crop makes a four-second rehearsal attempt. Technical checks pass. Sampled frames show the intended brow pinch and dropped gaze with stable face and room; the new shot is wider than the original target moment. It remains a test rather than an accepted replacement in the full trailer. Raw MOV and provenance are saved under clips/first/.

## Saved references

| File | Purpose |
|---|---|
| roy-stream-master-v1.png | Roy’s face, domestic setting, wardrobe, four-string ukulele and hand positions |
| fielder-reset-v1.png | Attentive reset before another practiced reaction |
| fielder-downward-glance-v1.png | End-pose reference guided by the actual v10 ~39s gesture |
| dan-fielder-monitor-clean-v1.png | Blank monitor plate with both men watching; screen corners available for compositing |
| pinterest-wrapper-v1.png | Code-authored fictional wrapper with exact title ROY FINDS HIS VOICE |

The first Roy generation had a six-string guitar-like instrument. It was rejected, and the selected edited reference corrects it to four strings and four tuners while preserving identity and setting. Original generation files remain in Codex’s generated-images directory; every selected project asset is copied here. The prompt history includes the rejected first attempt and the exact correction.

## What the previews establish

The reveal uses one Roy image continuously, authors the platform wrapper separately, and travels into a real-looking viewing room without swapping the man on the screen. The audio is an unbroken excerpt from D2-r1 at 104–122 seconds, with its accepted ElevenLabs performances and temporary plucked instrument. It is clearly labeled as a still-reference compositing test. Roy is not newly animated or lip-synced.

The Fielder reel first plays the actual source movement at source 2–6 seconds, then holds each generated pose for four seconds. It is a reference reel, not three completed takes. The final motion must preserve the original eyeline and framing; the generated landscape reference still needs alignment against the source.

## Rebuild

Use the bundled Python containing numpy and Pillow to run build_tests.py from any directory. It also needs ffmpeg and Liberation Sans. The script reads the original reaction clip and the accepted D2 mix, writes to build/first-trailer-visual-tests-v1/, and preserves the full trailer. Use verify_tests.py for rendered-artifact checks and the explicit two-second composition audit.

New moving performances require an accessible video workflow. Runway is installed, but its connector still fails with a missing link_id error. The user signed in to the website with Google. The browser confirms the Personal Standard workspace; the first silent Fielder test completed and was downloaded. One submission used 240 existing credits; Runway then awarded 300 onboarding credits, leaving 685. No additional purchase was made. See runway-generation-01.json for exact settings, prompt, references and the private session link.

## Integration access restored

The Runway app integration now authenticates successfully to the Daniel personal workspace and reports available video-generation models. This read-only check submitted no media generation. Further Runway generations remain deferred under the current GPT-first production preference. The browser fallback and saved motion test remain available.
