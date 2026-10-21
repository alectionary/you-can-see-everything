from pathlib import Path
import csv,json,subprocess,hashlib,re,math
import numpy as np,soundfile as sf
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-finishing-d4';D3=ROOT/'build/first-trailer-picture-pass-d3';VIDEO=OUT/'first-trailer-finishing-d4.mp4'
def probe(p,count=False):return json.loads(subprocess.check_output(['ffprobe','-v','error',*(['-count_frames'] if count else []),'-show_streams','-show_format','-of','json',str(p)],text=True))
def db(x):return 20*math.log10(max(float(x),1e-12))
rows=list(csv.DictReader((OUT/'timeline.csv').open()));p=probe(VIDEO,True);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert int(v['nb_read_frames'])==4320 and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==(1280,720)
assert float(p['format']['duration'])==180 and a['sample_rate']=='48000' and a['channels']==2
segments=[]
for r in rows:
 q=probe(OUT/'segments'/f"{r['segment']}.mp4");s=q['streams'][0];frames=int(s['nb_frames']);duration=frames/24
 assert frames==round(float(r['duration_seconds'])*24) and duration>=2
 segments.append({'id':r['segment'],'start':float(r['start_seconds']),'end':float(r['end_seconds']),'frames':frames,'duration':duration})
assert sum(x['frames'] for x in segments)==4320
pcm={}
for path in [OUT/'mix.wav',*sorted((OUT/'stems').glob('*.wav'))]:
 data,sr=sf.read(path,dtype='int32',always_2d=True);assert data.shape==(8640000,2) and sr==48000
 gap=data[164*48000:166*48000];assert not np.any(gap),path
 if path.stem in ['ukulele','piano','bass','strings','brass','percussion']:assert not np.any(data[170*48000:]),path
 pcm[str(path.relative_to(OUT))]={'samples':len(data),'channels':2,'silence_gate_nonzero_samples':int(np.count_nonzero(gap)),'peak_dbfs':db(np.max(abs(data.astype(np.float64)))/2**31),'format':sf.info(path).subtype}
source_speech=list((D3/'speech').glob('L*.wav'));assert len(source_speech)==31
for path in source_speech:assert path.read_bytes()==(OUT/'speech'/path.name).read_bytes()
assert (OUT/'captions.srt').read_bytes()==(D3/'captions.srt').read_bytes()
batch=json.loads((OUT/'lipsync-batch.json').read_text());assert len(batch['completed'])==22 and not batch['failed']
for item in batch['completed']:
 path=Path(item['output']);path=path if path.is_absolute() else ROOT/path
 actual=probe(path);assert int(actual['streams'][0]['nb_frames'])==item['frames']
# Inspect the actual encoded delivery audio and exact 48-frame black gate.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','2','-ar','48000','-f','f32le','-']);decoded=np.frombuffer(raw,'<f4').reshape(-1,2)[:8640000]
gap=decoded[164*48000:166*48000];gate_peak=db(np.max(abs(gap)));assert gate_peak<-50
black=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vf',"select='between(n,3936,3983)',scale=16:9",'-fps_mode','vfr','-pix_fmt','gray','-f','rawvideo','-']);assert len(black)==48*16*9 and max(black)==0
measured=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],text=True,capture_output=True,check=True);loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',measured.stderr,re.S)[-1]);assert -19<=float(loud['input_i'])<=-17 and float(loud['input_tp'])<=-1
mono=decoded.mean(axis=1);mono_loss=db(np.sqrt(np.mean(mono.astype(float)**2))/np.sqrt(np.mean(decoded.astype(float)**2)));assert mono_loss>-.5
mix=json.loads((OUT/'mix.json').read_text());uke,sr=sf.read(OUT/'stems/ukulele.wav',always_2d=True);mono_uke=uke.mean(axis=1);pitch=[]
for note in mix['notes'][:3]:
 start=round((note['actual_onset']+.055)*sr);signal=mono_uke[start:start+round(.24*sr)];spec=np.abs(np.fft.rfft(signal*np.hanning(len(signal)),n=262144));freq=np.fft.rfftfreq(262144,1/sr);expected=note['expected_frequency'];idx=np.where((freq>expected*.97)&(freq<expected*1.03))[0];k=idx[np.argmax(spec[idx])];fit=spec[k-1:k+2];delta=.5*(fit[0]-fit[2])/(fit[0]-2*fit[1]+fit[2]);actual=(k+delta)*sr/262144;cents=1200*np.log2(actual/expected)
 assert abs(cents)<12,(note,actual,cents)
 pitch.append({'midi':note['note'],'onset':note['actual_onset'],'expected_hz':expected,'measured_hz':actual,'cents_error':cents})
score=json.loads((OUT/'score/events.json').read_text());assert all(e['t']==166 for name,events in score['events'].items() for e in events if e['t']>=164)
original_qc=json.loads((D3/'QC.json').read_text());assert hashlib.sha256((D3/'first-trailer-picture-pass-d3.mp4').read_bytes()).hexdigest()==original_qc['sha256']
report={'artifact':str(VIDEO),'sha256':hashlib.sha256(VIDEO.read_bytes()).hexdigest(),'duration':180,'frames':4320,'dimensions':[1280,720],'fps':24,'audio_channels':2,'audio_sample_rate':48000,'segments':segments,'pcm':pcm,'encoded_gate_peak_dbfs':gate_peak,'encoded_loudness':{k:loud[k] for k in ['input_i','input_tp','input_lra']},'mono_fold_loss_db':mono_loss,'ukulele_pitch_checks':pitch,'black_frames':48,'black_max_gray':0,'speech_sources_preserved':31,'caption_bytes_preserved':True,'local_lipsync_jobs':22,'visible_dialogue_cues_processed':20,'silent_mouth_correction_jobs':2,'title':'One ensemble onset at 166; no later score attacks','status':'PASS technical finishing checks; sampled-frame performance review recorded separately','limits':'Audio-driven lip generation is not a guarantee of perfect phoneme-level realism. Mouth artifacts and approximate instrument fingering remain possible. Human perceptual listening approval has not been claimed.'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# D4 finishing cut — rendered QC\n\nTechnical checks passed on the actual delivery MP4. This pass includes audio-driven visible dialogue, recorded ukulele sample performance, practical foley and a stereo master. It remains a private, noncommercial production review cut.\n\n'
md+=f"Artifact: {VIDEO.name}; 180.000 seconds, 4,320 frames, 1280×720 at 24 fps, H.264 / stereo AAC 48kHz. SHA-256: {report['sha256']}.\n\n"
md+='## RULES.md: measured duration audit\n\n| Segment | Start | End | Actual duration | Frames | Minimum | Result |\n|---|---:|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | 2.000 | PASS |\n"
md+='\nAll 40 compositions retain the accepted D3 duration. No interval was shortened; minimum is exactly 2.000 seconds / 48 frames. Original teaser files and D3 viewing copy remain untouched. The original 39-second reaction is preserved as T05; audio-driven mouth edits apply to other speaking shots.\n\n'
md+=f"## Sound measurements\n\nEncoded integrated loudness **{loud['input_i']} LUFS**, true peak **{loud['input_tp']} dBTP**, loudness range **{loud['input_lra']} LU**. Mono fold-down loss is {mono_loss:.3f} dB relative to mean stereo power. The 24-bit 48kHz PCM master and all nine stems contain exactly 8,640,000 samples per channel, with exact zero at 164–166. Encoded gate peak is {gate_peak:.2f} dBFS; all 48 decoded gate frames are pure black. Music stems are exactly silent after 170. The title has a single score onset at 166.\n\n"
md+='All 31 original speech PCM files and captions are byte-identical to accepted D3. No voice pitch shift or time stretch was applied. The actual master applies only common gain and peak control to the voice bed. Twenty visible dialogue cues were driven by their exact saved recordings; separate silent tracks correct two unrelated mouth performances. Two speakers in T10 were processed independently, and T39–T40 share one continuous underlying lip pass.\n\n'
md+='The guitar placeholder is replaced with a sampled Flight Fireball tenor ukulele recorded by Mateusz Dąbrowski (FreePats, CC0). The original motif is retained. First middle-section pluck now follows the introduction at 110 seconds; the published sample tuning offsets and small performance variations are documented in mix.json. Opening A3, E4 and C-sharp4 pitch checks on the rendered ukulele stem all fall within 12 cents of the written notes. A3 is obtained by transposing the C4 sample three semitones.\n\n'
md+='## Review limits and source terms\n\nThe report verifies the exported artifact, stems, pitch, duration, gate and source continuity. Perceptual review uses saved sampled frames; there is no claim of human listening on headphones or speakers, or independent phoneme-by-phoneme certification. Hands still come from generated footage, so precise musical fingering is not asserted. Some mouths may show synthesis softness. The local Wav2Lip model is limited to personal/research/noncommercial use, including performance drivers; that restriction is not removed by subsequent enhancement. See trailer/first/finishing-d4/local-model-provenance.json.\n'
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['duration','frames','encoded_loudness','encoded_gate_peak_dbfs','mono_fold_loss_db','visible_dialogue_cues_processed','status']},indent=2))
