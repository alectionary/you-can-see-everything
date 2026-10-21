#!/usr/bin/env python3
"""Measure the exported animatic and its PCM stems; write QC.json and QC.md."""
from pathlib import Path
import argparse,csv,json,subprocess,wave,hashlib,re,math
import numpy as np
HERE=Path('/Users/anonymous/Documents/you-can-see-anything-teaser/trailer/first');ROOT=HERE.parents[1];OUT=ROOT/'build/first-trailer-picture-pass-d3'
parser=argparse.ArgumentParser();parser.add_argument('--voice-pass',action='store_true');args=parser.parse_args()
if args.voice_pass:OUT=ROOT/'build/first-trailer-voice-pass-d2'
VIDEO=OUT/'first-trailer-picture-pass-d3.mp4'
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
report={'artifact':str(VIDEO),'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'duration':180,'frames':4320,'dimensions':[1280,720],'fps':24,'segments':segments,'pcm':stems,'encoded_silence_peak_dbfs':db(np.max(abs(gap))),'black_frames':48,'black_max_gray':max(black),'encoded_loudness':{k:measure[k] for k in ['input_i','input_tp','input_lra']},'windows':windows,'speech':speech,'status':'PASS technical picture-pass checks; final lip sync and ukulele performance remain open'}

# Compare accepted principal speech and every score stem against D2-r1.
old=ROOT/'build/first-trailer-voice-pass-d2'
principal=[x for x in speech if x['speaker'] in ('DAN','ROY','FIELDER')]
assert len(principal)==22
assert not any(x['provider']=='macos' for x in speech)
for x in principal:assert (OUT/'speech'/(x['id']+'.wav')).read_bytes()==(old/'speech'/(x['id']+'.wav')).read_bytes(),x['id']
for name in ('ukulele','piano','bass','strings','brass','percussion','effects','ambience'):
 assert (OUT/'stems'/(name+'.wav')).read_bytes()==(old/'stems'/(name+'.wav')).read_bytes(),name
result_voice={'principal_cues':22,'principal_pcm_matches_accepted_d2_r1':True,'supporting_elevenlabs_cues':9,'macos_placeholders':0,'score_and_effect_stems_match_d2_r1':True}
report['voice_and_score_continuity']=result_voice
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# Full trailer picture pass D3 — rendered QC\n\nTechnical checks passed on the actual viewing MP4. This is a full picture workprint; generated mouth motion is not synchronized to the dialogue, and the ukulele SoundFont remains temporary.\n\n'
md+=f"Artifact: {VIDEO.name}. {report['duration']:.3f}s, {report['frames']} frames, 1280×720, 24fps, H.264/AAC 48kHz. SHA-256: {report['sha256']}.\n\n"
md+='## Measured composition audit against RULES.md\n\n| Segment | Start | End | Duration | Frames | Result |\n|---|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | PASS |\n"
md+='\nAll 40 compositions meet the 2.000-second minimum. No planned interval was shortened. The original teaser and accepted D2-r1 artifact are preserved.\n\n'
md+=f"## Sound and black gate\n\nEncoded loudness: {measure['input_i']} LUFS, {measure['input_tp']} dBTP, {measure['input_lra']} LU range. Master and nine stems have exactly 8,640,000 samples per channel, with exact PCM zero during 164–166 seconds. All 48 decoded picture frames in that gate are pure black. Encoded silence peak: {report['encoded_silence_peak_dbfs']} dBFS. All music stems are silent from 170 seconds.\n\n"
md+='All 31 dialogue cues have a recording and measured nonoverlapping active spans. All 22 principal PCM cues match accepted D2-r1 exactly, including the corrected question and longer “I was.” All eight score/effects/ambience stems match D2-r1 exactly. Nine supporting cues now use distinct ElevenLabs performances, with candidate A returning in the ukulele scene. No dialogue pitch or speed changes were applied.\n\n'
md+='## Picture continuity and limits\n\nT05 retains the source 2–6s reaction selected by the user. T06 and T07 use separate new practice performances. T28 and T34 show thumbnails extracted from the actual three edited takes. T23–T25 use one continuous Roy source, source frame n mapped to output frame n throughout the nested screen reveal; T39–T40 also continue one source take. Corporate review and distribution text are native, readable artwork. The lodge shot is inspected separately in VISUAL_REVIEW.md.\n\nGenerated speaking motion is provisional and often continues outside the audio windows. Final audio-driven facial performance is still required. The temporary nylon-guitar SoundFont is not a final ukulele performance, and finger-to-note synchronization is not claimed. Editor and monitor room bodies are still photographic plates with moving screen inserts. This is not final master approval. Full human listening and motion review remain useful before final delivery.\n'
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['duration','frames','encoded_silence_peak_dbfs','encoded_loudness','voice_and_score_continuity','status']},indent=2))
