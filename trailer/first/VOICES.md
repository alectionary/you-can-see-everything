# ElevenLabs character voices

Dan, Roy and Fielder use the recovered original teaser voices. Authentication, voice listing, history access and speech generation were verified on October 20, 2026. All three reference recordings exactly match the corresponding downloaded history audio after decoding to mono 48kHz signed 16-bit PCM. Their MP3 containers differ; the decoded performances do not.

| Character | ElevenLabs voice | Voice ID | Local continuity reference |
|---|---|---|---|
| Dan | Eric - Smooth, Trustworthy | cjVigY5qzO86Huf0OWal | dialogue/v2/d01.mp3 |
| Roy | Chris - Charming, Down-to-Earth | iP95p4xoKVk53GoZ742B | dialogue/v2/r01.mp3 |
| Fielder | Brian - Deep, Resonant and Comforting | nPczCjzI2devNBz1zQrb | dialogue/v2/f01.mp3 |

All three use **eleven_multilingual_v2**, with the settings recovered from the actual original generation history: stability 0.55, similarity boost 0.75, speed 1.0, style 0.0, speaker boost enabled. Preserve these as the first production baseline. A matching voice and settings do not make a new performance sample-identical or guarantee the same pacing.

Fielder’s earlier River and Roger generations are not the final voice. The Brian history recording matches the final local f01 file exactly after decoding; the Roger recording does not. No voice cloning or impersonation is required.

## New continuity samples

- [Dan’s current production line](../../dialogue/first/dan_L19_platform.mp3): “I’d like the conversation to happen on Pinterest.” The initial dan_L19 voice test is retained as a superseded script sample.
- [Roy](../../dialogue/first/voice-tests/roy_L01.mp3): “Sorry. Let me start again.”
- [Fielder](../../dialogue/first/voice-tests/fielder_L02.mp3): “What made you start doing this?”

The initial three voice checks used 86 text characters. The corrected Dan platform-motive line is a separate 49-character production request. Sample metadata and decode checks are saved beside the audio. These samples establish working API access and the recovered voice configuration; naturalness, emotional restraint and fit against the picture still need listening review. No speed or pitch processing was applied to the samples.

## Configuration and credential handling

[voices.json](voices.json) stores the voice IDs, model, settings and project-specific history references. [voice-continuity.json](voice-continuity.json) records the successful PCM comparison results. Neither file contains the API key.

[elevenlabs_tts.py](elevenlabs_tts.py) reads the credential directly from the existing macOS Keychain entry. It can also accept an explicitly supplied ELEVENLABS_API_KEY environment variable. It never writes the credential to disk or passes it on a command line. The only authenticated destination is https://api.elevenlabs.io.

Example from the repository root, with a fresh output name:

```sh
python3 trailer/first/elevenlabs_tts.py --character DAN --text 'Roy chose the song.' --output dialogue/first/dan_L22.mp3
```

This spends account credits. Identical requests reuse a cached output with matching provenance; the helper refuses to overwrite a different or unverified existing output. Failed API responses are reported by status without exposing credentials. Generation timing is nondeterministic, so inspect each new performance before cutting it into the trailer.

The original trailer MP4, v7/v10 subtitles and teaser recordings remain untouched. D2 now uses this configuration for all 22 principal-character cues; D1 retains its earlier placeholders. See VOICE_PASS.md for the generated-line manifest, preserved original recordings and rendered verification. The three Roy candidates, communications employee, editor and offscreen production roles still need their own casting choices.

## API references

- [Generation history and recorded settings](https://elevenlabs.io/docs/api-reference/history/get)
- [History audio retrieval](https://elevenlabs.io/docs/api-reference/history/get-audio)
- [Text to speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
