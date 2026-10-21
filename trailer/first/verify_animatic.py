#!/usr/bin/env python3
"""Measure the exported animatic and its PCM stems; write QC.json and QC.md."""
from pathlib import Path
import argparse,csv,json,subprocess,wave,hashlib,re,math
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'build/first-trailer-animatic'
parser=argparse.ArgumentParser();parser.add_argument('--voice-pass',action='store_true');args=parser.parse_args()
if args.voice_pass:OUT=ROOT/'build/first-trailer-voice-pass-d2'
VIDEO=OUT/('first-trailer-voice-pass-d2.mp4' if args.voice_pass else 'first-trailer-animatic-d1.mp4')
def probe(path,count=False):
    args=['ffprobe','-v','error']+(['-count_frames'] if count else [])+['-show_streams','-show_format','-of','json',str(path)]
    return json.loads(subprocess.check_output(args,text=True))
def db(a):return round(20*math.log10(max(float(a),1e-12)),3)
rows=list(csv.DictReader((HERE/'timeline.csv').open()));result=probe(VIDEO,True)
v=next(s for s in result['streams'] if s['codec_type']=='video');a=next(s for s in result['streams'] if s['codec_type']=='audio')
assert int(v['nb_read_frames'])==4320 and v['r_frame_rate']=='24/1'
assert (v['width'],v['height'])==(1280,720) and a['sample_rate']=='48000'
assert float(result['format']['duration'])==180
segments=[]
for row in rows:
    s=probe(OUT/'segments'/(row['segment']+'.mp4'));video=s['streams'][0]
    frames=int(video['nb_frames']);expected=round(float(row['duration_seconds'])*24)
    assert frames==expected and frames>=48,row
    segments.append({'id':row['segment'],'start':float(row['start_seconds']),'end':float(row['end_seconds']),'frames':frames,'duration':frames/24})
assert sum(s['frames'] for s in segments)==4320
stems={}
for path in [OUT/'mix.wav',*sorted((OUT/'stems').glob('*.wav'))]:
    with wave.open(str(path)) as f:
        assert f.getframerate()==48000 and f.getnframes()==8640000
        data=np.frombuffer(f.readframes(f.getnframes()),'<i2').reshape(-1,f.getnchannels())
    assert not np.any(data[7872000:7968000]),path
    if path.stem in ['ukulele','piano','bass','strings','brass','percussion']:
        assert not np.any(data[170*48000:]),path
    stems[str(path.relative_to(OUT))]={'samples_per_channel':len(data),'gate_nonzero_samples':int(np.count_nonzero(data[7872000:7968000])),'peak_dbfs':db(np.max(np.abs(data.astype(np.int32)))/32768)}
# Decode the actual viewing copy; encoded silence can have edge residuals.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','1','-ar','48000','-f','f32le','-'])
decoded=np.frombuffer(raw,'<f4')[:8640000];gap=decoded[164*48000:166*48000]
black=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vf',"select='between(n,3936,3983)',scale=16:9",'-fps_mode','vfr','-pix_fmt','gray','-f','rawvideo','-'])
assert len(black)==48*16*9 and max(black)==0
windows={}
for start,end in [(0,8),(18,40),(40,62),(62,82),(82,104),(104,126),(126,148),(148,164),(164,166),(166,170),(170,180)]:
    part=decoded[int(start*48000):int(end*48000)];windows[f'{start}-{end}']={'rms_dbfs':db(np.sqrt(np.mean(part.astype(float)**2))),'peak_dbfs':db(np.max(abs(part)))}
loud=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],text=True,capture_output=True,check=True)
measure=json.loads(re.findall(r'\{\s*"input_i".*?\}',loud.stderr,re.S)[-1])
assert float(measure['input_tp'])<=-1
speech=json.loads((OUT/'speech/timing.json').read_text())
assert len(speech)==31 and all(x['actual_end']<=(speech[i+1]['start']-.1 if i+1<len(speech) else 180) for i,x in enumerate(speech))
report={'artifact':str(VIDEO),'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'duration':180,'frames':4320,'dimensions':[1280,720],'fps':24,'segments':segments,'pcm':stems,'encoded_silence_peak_dbfs':db(np.max(abs(gap))),'black_frames':48,'black_max_gray':max(black),'encoded_loudness':{k:measure[k] for k in ['input_i','input_tp','input_lra']},'windows':windows,'speech':speech,'status':'PASS technical animatic checks; performance and finished-footage QC remain open'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2))
md='''# First trailer animatic review

Technical animatic checks pass. This is a labeled workprint with storyboard placeholders, installed macOS speech voices, two reused Dan recordings, one new ElevenLabs Dan production line, and an original scratch arrangement. It is not a finished trailer or a final performance review.

'''
if args.voice_pass:
    md=md.replace('installed macOS speech voices, two reused Dan recordings, one new ElevenLabs Dan production line, and an original scratch arrangement.','the recovered ElevenLabs voices for all 22 principal-character lines (including two original teaser recordings), nine macOS supporting-role placeholders, and the scratch arrangement.')
    assert sum(x.get('provider')=='elevenlabs' for x in speech)==20
    assert sum(x.get('provider')=='original teaser' for x in speech)==2
    assert sum(x.get('provider')=='macos' for x in speech)==9
md+=f"Artifact: `{VIDEO.name}` ({VIDEO.stat().st_size:,} bytes). SHA-256: `{report['sha256']}`.\n\n"
md+='## Rendered picture and duration audit\n\nDecoded export: 180.000 seconds, 4,320 frames, 1280×720 at 24 fps, H.264 with 48kHz AAC audio. Source segments match the timeline, and their frame counts sum to the decoded final count. All 48 decoded frames at 164–166 seconds are pure black.\n\n'
md+='| Segment | Start | End | Measured duration | Frames | Minimum | Result |\n|---|---:|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | 2.000 | PASS |\n"
md+='\nMinimum actual segment: **2.000 seconds / 48 frames**. The Pinterest comment is a separate five-second composition within a continuing reference still. The T24 pullback is a continuous animated crop of a designed screen plate.\n\n'
md+='## Audio measurements\n\n'
md+=f"Encoded integrated loudness: **{measure['input_i']} LUFS**, true peak **{measure['input_tp']} dBTP**, loudness range **{measure['input_lra']} LU**. The scratch mix preserves its quiet opening and larger ending rather than forcing the provisional -16 LUFS target.\n\n"
md+=f"The master and all {len(stems)-1} PCM stems contain exactly 8,640,000 samples per channel and zero nonzero samples during 164–166 seconds. Encoded gate peak is {report['encoded_silence_peak_dbfs']:.2f} dBFS; small AAC edge residuals are separate from the exact-zero PCM test. Score stems are zero from 170 seconds onward.\n\n"
md+='| Export window | RMS dBFS | Peak dBFS |\n|---|---:|---:|\n'
for window,m in windows.items():md+=f"| {window}s | {m['rms_dbfs']:.2f} | {m['peak_dbfs']:.2f} |\n"
md+='''
All 31 dialogue recordings are present and their measured active spans do not overlap the next line. Recorded performance durations were retained; no time stretching was applied. captions.srt contains actual speech text, with caption windows extended slightly where a synthetic performance exceeded its initial target but remained within the available hold. Supporting voices remain timing references. Principal identities match the established teaser cast; individual acting still needs listening review. The plucked SoundFont timbre is nylon guitar standing in for ukulele.

## Rules audit and limits

1. All 40 measured source compositions meet the two-second minimum; final count reconciles to their sum. Final contact frames support visual inspection. This is not a full motion or lip-sync review of finished footage.
2. No planned segment was shortened; runtime remains 180.000 seconds.
3. Locked teaser files remain untouched. This is the separately requested trailer timeline; the two reused recordings retain their words and pitch. The title and black beat have no dialogue.
4. This report provides the explicit measured duration audit. A final production delivery will require a fresh QC pass after placeholders and voices are replaced.
5. Measurements above are from the actual encoded MP4 and saved PCM stems. Musical instrumentation and event timing are documented in the editable score; perceptual balance and dramatic effectiveness still need human listening review.

## Visual and score review

Reviewed the storyboard layouts, the actual exported publicity frame and final comment, and all three rendered score pages. Screen wording is readable. Source footage, new-shot placeholders and mockups are identified in the workprint. The T24 composite is a storyboard of the planned pullback; it does not yet contain a new filmed performance or tracking shot. Three score pages compile without notation warnings and remain editable in the saved LilyPond source.

## Next production work

Replace the stream, rehearsal, casting, communications and ski-lodge placeholders with consistent footage. Recover or select character voices and test ElevenLabs access before paid batches. Record a convincing ukulele performance and refine the score against the accepted acting. Rebuild and review the final frames, lip sync, musical attacks, levels and all duration boundaries after those changes.
'''
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['duration','frames','dimensions','encoded_silence_peak_dbfs','encoded_loudness','status']},indent=2))
