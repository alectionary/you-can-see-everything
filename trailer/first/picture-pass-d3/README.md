# Full trailer picture pass D3

The complete 180-second picture workprint is `build/first-trailer-picture-pass-d3/first-trailer-picture-pass-d3.mp4`. D2-r1 and the original teaser are preserved. No commits or pushes were made.

This pass replaces the character and lodge storyboards with generated moving footage, inserts the original food-bank and demolition material, and builds the corporate graphics and nested Pinterest reveal. The monitor-room and editor-room bodies remain photographic plates with composed screens. It is a picture workprint, not the finished master.

All 31 dialogue cues now use ElevenLabs or the original teaser recordings. The 22 accepted principal PCM cues, including the revised question and longer “I was,” are preserved exactly. Nine supporting lines have distinct voices, with candidate A returning in the ukulele scene. `support-voices.json` records their provenance. The principal registry remains unchanged.

`motion-assets.json` records 14 Runway generations, exact prompts, task IDs, local paths, hashes, and measured media metadata. This pass used 1,020 credits from a starting balance of 2,310, leaving 1,290. The approved 1,800-credit picture-pass target and 510-credit reserve were respected. No plan changes or purchases were made. Image provenance and exact prompts are in `image-assets.json`; the first lodge draft and six-peg instrument draft are retained there as superseded references.

## Reproduce

Use the bundled Python with Pillow and numpy, plus ffmpeg:

```sh
python build_picture.py audio picture export
python verify_picture.py
```

Run from this directory or supply absolute paths. The builder resolves media against the local repository. It skips existing picture segments; remove only a segment that needs rebuilding. It never regenerates API media. The audio source CSV is local to this pass and retains the accepted D2-r1 principal sources.

## Finishing work

The generated actors are not yet synchronized to the exact spoken phonemes. Replace their provisional speaking movement with audio-driven facial performances; preserve approved voice pitch and natural duration. In particular, the short apology, rehearsal questions, candidates, corporate answers, Dan interviews, and final webcam question need this treatment.

The score remains the accepted editable arrangement, with sparse plucked notes, discordant piano, increasing bass and ensemble pressure, exact silence at 164–166 seconds, a single title attack at 166, and no music after 170. The plucked SoundFont is still nylon guitar standing in for ukulele. A final four-string performance and finger-to-note alignment remain open. Event and room foley can be refined once the picture is accepted.

Generated lodge mechanics and hands are provisional. The painting now visibly descends through the frame; individual shred shapes can be refined in a finishing shot. The premise stays ambiguous: Pinterest benefits from Roy’s sincere music without proof that Dan wrote or staged it.

## Rule audit

The 40 planned compositions retain their original durations, all at least two seconds. No shot was shortened to fund another. The teaser dialogue/subtitles remain locked; this is the separately approved full trailer. The rendered QC report lists every segment with measured frames and duration and checks the actual exported MP4, exact PCM gate, title black, sound levels, and accepted-source continuity.
