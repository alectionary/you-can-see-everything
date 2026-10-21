# First trailer principal voice pass

D2 replaces all Dan, Roy and Fielder placeholders with their recovered ElevenLabs voices. The original D1 MP4 and its components remain in build/first-trailer-animatic/. This is still a storyboard workprint: nine supporting-role cues use macOS voices, and new scenes remain placeholders.

- [Watch D2 revision 1](../../build/first-trailer-voice-pass-d2/first-trailer-voice-pass-d2-r1.mp4)
- [Dialogue stem](../../build/first-trailer-voice-pass-d2/stems/dialogue.wav)
- [Rendered QC](../../build/first-trailer-voice-pass-d2/QC.md)
- [Contact sheet](../../build/first-trailer-voice-pass-d2/contact-sheet.jpg)
- [Generation manifest](principal-dialogue-pass.json)

## Fielder revision 1 — pronunciation and pacing

User listening feedback flagged a stray “nuh” after the opening question and an overly clipped “I was.” Both takes were regenerated with the established Brian voice, using the same spoken words. L08 active speech increased from approximately 0.31 to 0.91 seconds; the placed clip is 1.06 seconds including preserved low-level tail. Its caption and music duck now extend through 38.6 seconds within the existing three-second picture hold. L02 has a fresh generation with a gentler delivery. Revisions keep 30 ms head and 140 ms tail padding where the source allows it, rather than trimming weak ending sounds at the tighter default threshold.

The previous MP4, dialogue stem, mix, captions, timings and QC are retained in build/first-trailer-voice-pass-d2/revisions/before-fielder-r1/. Revised source audio and request metadata live in dialogue/first/revisions/fielder-r1/. Request headers report 37 text characters for these two takes; immediate account usage counts can lag. Future principal batches preserve explicitly selected, provenance-verified takes with per-line settings.

The revised render passes the 180-second/4,320-frame checks, all 40 shot minimums, speech spacing, exact PCM silence and true peak checks. These are technical checks; the replacement pronunciation remains open to user listening review.

## Voice continuity

| Character | Voice | Model |
|---|---|---|
| Dan | Eric | eleven_multilingual_v2 |
| Roy | Chris | eleven_multilingual_v2 |
| Fielder | Brian | eleven_multilingual_v2 |

Baseline settings are stability 0.55, similarity boost 0.75, speed 1.0, style 0.0 and speaker boost enabled. Revision 1 uses per-line speed 0.88 for L02 and 0.72 for L08, with conversational context for L08. Principal lines comprise 20 new-trailer ElevenLabs recordings and two original teaser recordings. Seventeen recordings were generated in this pass; three existing matching recordings were reused. Every generated source has saved request metadata. This pass used 257 included credits for 507 new text characters; the account reported 8,987 remaining after the batch.

## Timing and mix

All 22 principal performances fit their available holds at their recorded duration. No time stretching, pitch correction or picture-segment shortening was applied. Dialogue was trimmed at low-level head/tail silence, gently faded at the edges and peak-balanced for the scratch mix. Cue placements remain those in dialogue.csv; subtitles retain the requested words and cover the target holds. Individual short utterances can finish before their captions disappear.

The corrected Fielder squint/downward glance remains the rehearsal reference. Dan’s platform line is “I’d like the conversation to happen on Pinterest.” The existing score arrangement and 164–166 second silence are preserved; the sound mix is rebuilt against the new dialogue.

## Rendered verification

Export: **180.000 seconds, 4,320 frames, 1280×720 at 24 fps**. All 40 picture segments meet the two-second minimum. Every PCM stem and the master pass the exact-zero 164–166 gate. Revision 1 encoded loudness is -20.59 LUFS integrated, with -1.70 dBTP true peak.

Inspected the actual exported contact sheet and selected frames for the reaction, platform line, Pinterest reveal and final Roy question. The source manifest verifies that no macOS principal line remains. These checks do not establish acting quality, perfect pronunciation or final lip sync; those need listening and later footage review. The nine supporting cues and guitar-based ukulele stand-in are still temporary.

## Rebuilding

Generate only missing principal lines, with caching and a quota check:

```sh
python3 trailer/first/principal_dialogue_pass.py --generate
```

The command without --generate performs a dry run and makes no API request. Then use the bundled Python with numpy and Pillow:

```sh
/Users/anonymous/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 trailer/first/build_animatic.py --voice-pass --phase all
/Users/anonymous/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 trailer/first/verify_animatic.py --voice-pass
```

New output remains in build/first-trailer-voice-pass-d2/. Future timing changes must extend picture holds and musical gates consistently rather than speeding up dialogue to fit. Credentials stay in Keychain or an explicitly injected environment variable; no API key is saved in this package.
