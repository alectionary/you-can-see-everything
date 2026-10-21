"""Verify the actual D6 delivery, including mouth closure, new score timing and every picture hold."""
from pathlib import Path
import csv,hashlib,json,math,re,struct,subprocess
import cv2,numpy as np,soundfile as sf
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-revision-d6';D4=ROOT/'build/first-trailer-finishing-d4';D5=ROOT/'build/first-trailer-ukulele-d5';VIDEO=OUT/'first-trailer-revision-d6.mp4';SR=48000;N=191*SR
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def db(x):return 20*math.log10(max(float(x),1e-12))
def probe(p,count=False):return json.loads(subprocess.check_output(['ffprobe','-v','error',*(['-count_frames'] if count else []),'-show_streams','-show_format','-of','json',str(p)],text=True))
rows=list(csv.DictReader((OUT/'timeline.csv').open()));oldrows={r['segment']:r for r in csv.DictReader((D4/'timeline.csv').open())};p=probe(VIDEO,True);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert int(v['nb_read_frames'])==4584 and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==(1280,720)
assert float(p['format']['duration'])==191 and a['sample_rate']=='48000' and a['channels']==2
segments=[];cursor=0
for row in rows:
 s=probe(OUT/'segments'/f"{row['segment']}.mp4")['streams'][0];frames=int(s['nb_frames']);d=frames/24
 assert frames==round(float(row['duration_seconds'])*24) and d>=2 and float(row['start_seconds'])==cursor
 if row['segment'] in oldrows:assert d==float(oldrows[row['segment']]['duration_seconds'])
 segments.append({'id':row['segment'],'start':cursor,'end':cursor+d,'duration':d,'frames':frames});cursor+=d
assert cursor==191 and len(segments)==44
for folder,name in [(D4,'first-trailer-finishing-d4.mp4'),(D5,'first-trailer-ukulele-d5.mp4')]:assert sha(folder/name)==json.loads((folder/'QC.json').read_text())['sha256']
timing=json.loads((OUT/'speech/timing.json').read_text());dialogue=list(csv.DictReader((OUT/'dialogue.csv').open()));assert len(timing)==32
for f in (D4/'speech').glob('L*.wav'):
 name='L04b.wav' if f.stem=='L04' else f.name;assert sha(f)==sha(OUT/'speech'/name)
assert [e['speaker'] for e in timing if e['id'] in ['L04a','L04b']]==['DAN','DAN']
assert next(e for e in dialogue if e['line_id']=='L04a')['text']=='Why would I deceive you?'
cards=[s for s in segments if s['id'].startswith('C')];assert [(s['start'],s['end']) for s in cards]==[(79,81),(106,108),(168,171),(187,191)]
for card in cards:
 assert not any(e['start']<card['end'] and e['caption_end']>card['start'] for e in timing)
pcm={};music_names=['roy','plucks','low','bloom','grit','body','reverse']
for f in [OUT/'mix.wav',OUT/'music-only.wav',*sorted((OUT/'stems').glob('*.wav'))]:
 z,sr=sf.read(f,dtype='int32',always_2d=True);assert z.shape==(N,2) and sr==SR and sf.info(f).subtype=='PCM_24'
 assert not np.any(z[171*SR:173*SR]),f
 if f.stem in music_names or f.name=='music-only.wav':assert not np.any(z[177*SR:]),f
 if f.stem in music_names and f.stem!='roy':assert not np.any(z[:18*SR]),f
 pcm[str(f.relative_to(OUT))]={'frames':len(z),'channels':2,'sample_rate':sr,'gap_nonzero_samples':0,'peak_dbfs':db(np.max(abs(z.astype(float)))/2**31)}
del z
music,sr=sf.read(OUT/'music-only.wav',always_2d=True);card_music=[]
for lo,hi in [(79,81),(106,108),(168,171)]:
 rms=db(np.sqrt(np.mean(music[round(lo*SR):round(hi*SR)]**2)));assert rms>-55
 card_music.append({'start':lo,'end':hi,'premaster_rms_dbfs':rms})
newroy,sr=sf.read(OUT/'stems/roy.wav',always_2d=True);oldroy,sr=sf.read(D5/'stems/roy.wav',always_2d=True)
boost=db(np.sqrt(np.mean(newroy[SR:round(3.4*SR)]**2))/np.sqrt(np.mean(oldroy[SR:round(3.4*SR)]**2)));assert boost>3
assert np.max(abs(newroy[:18*SR]))>np.max(abs(oldroy[:18*SR]))
# The middle performance moves by four seconds and remains identical to quantization precision.
middle_error=np.max(abs(newroy[114*SR:130*SR]-oldroy[110*SR:126*SR]));assert middle_error<2e-7
del music,newroy,oldroy
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','2','-ar',str(SR),'-f','f32le','-']);decoded=np.frombuffer(raw,'<f4').reshape(-1,2)[:N];assert len(decoded)==N and np.isfinite(decoded).all()
gate=db(np.max(abs(decoded[171*SR:173*SR])));assert gate<-50
r=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1]);assert -19<=float(loud['input_i'])<=-17 and float(loud['input_tp'])<=-1
mono=decoded.mean(axis=1);fold=db(np.sqrt(np.mean(mono.astype(float)**2))/np.sqrt(np.mean(decoded.astype(float)**2)));assert fold>-.5
black=subprocess.check_output(['ffmpeg','-v','error','-ss','171','-i',str(VIDEO),'-t','2','-vf','scale=16:9','-pix_fmt','gray','-f','rawvideo','-']);assert len(black)==48*16*9 and max(black)==0
pitch=[]
for t,n in [(1.09,57),(3.12,61)]:
 expected=440*2**((n-69)/12);x=mono[round(t*SR):round((t+.24)*SR)];sp=np.abs(np.fft.rfft(x*np.hanning(len(x)),n=262144));freq=np.fft.rfftfreq(262144,1/SR);ids=np.where((freq>expected*.97)&(freq<expected*1.03))[0];k=ids[np.argmax(sp[ids])];y=sp[k-1:k+2];delta=.5*(y[0]-y[2])/(y[0]-2*y[1]+y[2]);hz=(k+delta)*SR/262144;cents=1200*np.log2(hz/expected);assert abs(cents)<15
 pitch.append({'source':'Actual decoded MP4 opening chord','window_start':t,'midi':n,'expected_hz':expected,'measured_hz':hz,'cents_error':cents})
# Check the restored Dan words in the actual AAC delivery against their saved speech waveforms.
speech_correlation=[]
for lid in ['L04a','L04b']:
 item=next(e for e in timing if e['id']==lid);voice,sr=sf.read(OUT/'speech'/f'{lid}.wav');assert sr==SR
 z=mono[round(item['start']*SR):round(item['start']*SR)+len(voice)];corr=float(np.corrcoef(z,voice)[0,1]);assert corr>.94,(lid,corr)
 speech_correlation.append({'id':lid,'speaker':'DAN','actual_delivery_correlation_with_source':corr})
del raw,decoded,mono
events=json.loads((OUT/'score/events.json').read_text());assert events['duration_seconds']==191
for role,es in events['events'].items():
 for e in es:assert e['t']+e['d']<=171 or e['t']==173
 assert all(e['t']==173 for e in es if e['t']>=171)
assert any(e['t']==113.5 for e in events['events']['low']) and any(e['t']==114 for e in events['events']['roy'])
# Verify MIDI end tick, pitches, durations, velocities and tempo independently.
data=(OUT/'score/ukulele-score-d6.mid').read_bytes();fmt,ntr,division=struct.unpack('>HHH',data[8:14]);assert (fmt,ntr,division)==(1,8,480)
def vlq(d,j):
 value=0
 while True:
  c=d[j];j+=1;value=(value<<7)|(c&127)
  if c<128:return value,j
pos=14;tracks=[]
for tr in range(ntr):
 assert data[pos:pos+4]==b'MTrk';length=struct.unpack('>I',data[pos+4:pos+8])[0];chunk=data[pos+8:pos+8+length];pos+=8+length;j=0;tick=0;ons=[];offs=[];tempos=[]
 while j<len(chunk):
  dt,j=vlq(chunk,j);tick+=dt;status=chunk[j];j+=1
  if status==255:
   typ=chunk[j];j+=1;n,j=vlq(chunk,j);payload=chunk[j:j+n];j+=n
   if typ==81:tempos.append(int.from_bytes(payload,'big'))
  elif status>>4 in [8,9]:
   note,velocity=chunk[j:j+2];j+=2;(ons if status>>4==9 and velocity else offs).append((tick,note,velocity))
  elif status>>4==12:j+=1
  else:raise ValueError(status)
 assert tick==191*480
 tracks.append((ons,offs,tempos))
assert tracks[0][2]==[1000000]
for (role,es),(ons,offs,_) in zip(events['events'].items(),tracks[1:]):
 assert sorted(ons)==sorted((round(e['t']*480),n,e['v']) for e in es for n in e['notes']),role
 assert sorted(offs)==sorted((round((e['t']+e['d'])*480),n,0) for e in es for n in e['notes']),role
# Actual delivered silent mouths must match their tracked neutral patches, while upper faces retain motion.
mouth_checks=[]
for name in ['T04','T08','T10','T22','T26','T30']:
 meta=json.loads((OUT/'mouths'/f'{name}.json').read_text());weights=np.load(OUT/'mouths'/f'{name}.speech-weights.npy');boxes=np.load(OUT/'mouths'/f'{name}.face-boxes.npy');tracking={r['frame']:r for r in json.loads((OUT/'mouths'/f'{name}.tracking.json').read_text())}
 source=cv2.VideoCapture(str(D4/'segments'/f'{name}.mp4'));source.set(cv2.CAP_PROP_POS_FRAMES,meta['reference_frame']);okay,reference=source.read();assert okay
 x1,y1,x2,y2=boxes[meta['reference_frame']];rw=x2-x1;rh=y2-y1;yy,xx=np.mgrid[:720,:1280];cx=.74 if x2<700 else .50;rx=.27 if x2<700 else .31
 radius=np.sqrt(((xx-(x1+rw*cx))/(rw*rx))**2+((yy-(y1+rh*.765))/(rh*.115))**2);refmask=(radius<.5).astype(np.uint8)
 actual=cv2.VideoCapture(str(VIDEO));global_start=round(next(s['start'] for s in segments if s['id']==name)*24);errors=[];baseline=[];upper=[]
 chosen=[i for i,w in enumerate(weights) if w==0 and i%3==0]
 for i in chosen:
  transform=np.array(tracking[i]['matrix'],np.float32);refwarp=cv2.warpAffine(reference,transform,(1280,720),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT);mask=cv2.warpAffine(refmask,transform,(1280,720),flags=cv2.INTER_NEAREST)>0
  actual.set(cv2.CAP_PROP_POS_FRAMES,global_start+i);okay,f=actual.read();assert okay;source.set(cv2.CAP_PROP_POS_FRAMES,i);okay,old=source.read();assert okay
  errors.append(float(np.mean(abs(f[mask].astype(float)-refwarp[mask].astype(float)))));baseline.append(float(np.mean(abs(old[mask].astype(float)-refwarp[mask].astype(float)))))
  bx,by,be,bottom=boxes[i];ymax=round(by+(bottom-by)*.64);upper.append(float(np.mean(abs(f[by:ymax,bx:be].astype(float)-old[by:ymax,bx:be].astype(float)))))
 actual.release();source.release();assert len(errors)>=3 and np.median(errors)<8,(name,errors)
 assert np.median(upper)<5,(name,upper)
 mouth_checks.append({'segment':name,'silent_frames_checked_in_actual_mp4':len(errors),'median_neutral_mouth_error_8bit':float(np.median(errors)),'prior_mouth_error_8bit':float(np.median(baseline)),'upper_face_preservation_error_8bit':float(np.median(upper)),'closure_tail_seconds':meta['closure_tail_seconds']})
# Scene scan detects no cut inside a held composition. All approved boundaries remain at least two seconds apart.
scan=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-an','-vf',"select='gt(scene,0.25)',showinfo",'-f','null','-'],text=True,capture_output=True,check=True)
cuts=[float(x) for x in re.findall(r'pts_time:([0-9.]+)',scan.stderr)];boundaries=[s['start'] for s in segments];unplanned=[t for t in cuts if min(abs(t-b) for b in boundaries)>1.1/24];assert not unplanned,unplanned
info=subprocess.check_output(['pdfinfo',str(OUT/'score/ukulele-score-d6.pdf')],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);assert pages==6
compile_log=(OUT/'score/compile.log').read_text();assert 'successfully completed' in compile_log and 'warning:' not in compile_log.lower()
report={'status':'PASS rendered technical checks; sampled-frame review documented separately','artifact':str(VIDEO),'sha256':sha(VIDEO),'duration_seconds':191,'frames':4584,'dimensions':[1280,720],'fps':24,'added_seconds':11,'segments':segments,'minimum_segment_seconds':min(s['duration'] for s in segments),'cards':cards,'encoded_loudness':{k:loud[k] for k in ['input_i','input_tp','input_lra']},'mono_fold_loss_db':fold,'encoded_gap_peak_dbfs':gate,'black_frames':48,'black_max_gray':0,'pcm':pcm,'opening_strum_rms_increase_db':boost,'middle_roy_max_pcm_error':float(middle_error),'card_music_energy':card_music,'pitch_checks':pitch,'dan_opening_source_correlations':speech_correlation,'dan_mouth_checks':mouth_checks,'original_speech_files_preserved':31,'spoken_cues':32,'new_spoken_cues':1,'midi_tracks':ntr,'midi_matches_event_map':True,'score_pdf_pages':pages,'score_pdf_sha256':sha(OUT/'score/ukulele-score-d6.pdf'),'scene_changes':cuts,'unplanned_internal_cuts':unplanned,'earlier_cuts_preserved':True,'builtin_image_generations':3,'new_runway_generations':0,'new_elevenlabs_generations':0,'limits':'Silent-mouth correction preserves upper-face/head motion but is not a guarantee of perfect phonemes during speech. Hands remain approximate generated performance. Perceptual headphone/speaker approval is not claimed.'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# D6 user-notes revision - rendered QC\n\nThe exported MP4 passes technical checks: 191.000 seconds, 4,584 frames, 1280 x 720 at 24 fps, stereo AAC 48 kHz. Earlier D4 and D5 exports retain their verified hashes.\n\n'
md+='## RULES.md audit\n\nAll forty original picture holds retain their durations. Four standalone cards add eleven seconds; no interval funds another. Minimum hold remains 2.000 seconds. The actual export was scene-scanned; detected cuts match planned boundaries within one frame, with no unplanned internal cut. Dialogue and captions shift with the inserted cards. The only new speech is the explicitly requested original Dan question, with the assurance moved later inside the same four-second shot. All thirty-one accepted speech PCM files survive unchanged except for the documented renaming of L04 to L04b. No voice is sped up or pitch shifted. Cards do not overlap any spoken-caption window.\n\n| Segment | Start | End | Actual duration | Frames | Minimum | Result |\n|---|---:|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | 2.000 | PASS |\n"
md+=f"\n## Audio\n\nActual encoded loudness {loud['input_i']} LUFS, true peak {loud['input_tp']} dBTP, range {loud['input_lra']} LU. Mono fold change {fold:.4f} dB. All ten PCM stems, music-only render and master have exactly 9,168,000 frames and exact silence 171-173. The decoded AAC gap peak is {gate:.2f} dBFS. All 48 corresponding video frames are pure black. The title has one score onset at 173; all music ends by 177. CTA 187-191 is deliberately silent.\n\n"
md+=f"Opening strum RMS is {boost:.2f} dB above the D5 clean instrument stem, before nearly identical common master gains. Four-string staggered chords replace thin single-note plucks. No other musical stem plays in the first eighteen seconds. The encoded delivery's A3 and wrong C-sharp were pitch checked within fifteen cents. Roy's middle performance remains identical after its four-second shift, to within {middle_error:.3g} PCM amplitude. Music energy is present during each inserted mid-trailer card; notation and bass/texture/rhythm events were extended rather than stretching dialogue or the complete soundtrack. The delivered MIDI was parsed independently and its 191-second duration, tempo, note onsets, releases and velocities agree with the written event map.\n\n"
md+='## Dan and documents\n\nBoth original Dan recordings are restored in T04: d04 question followed by d05 assurance. The actual AAC delivery correlates above 0.94 with each saved speech source. Six Dan shots use tracked neutral lower-mouth patches outside his real speech windows, closing within 100 ms. The actual final MP4 is sampled in those windows: lip pixels agree with the intended neutral reference and upper-face pixels retain the source performance. This checks delivery selection and silent-mouth behavior; it does not certify perfect phoneme articulation.\n\nThree clean digital documents are replaced with built-in GPT-generated physical props: folded preparation printout, reflected phone photo of the communications screen, and scuffed distribution printout. Reference images, final PNGs and prompt provenance are saved under trailer/first/revision-d6/images/. Important Pinterest communications wording is retained. These are fictional trailer props.\n\n## Score and review limits\n\nThe revised six-page LilyPond production score compiles without warnings. All pages were rendered to PNG and visually reviewed. The performance score shows transformed sounding pitches; it is not a playable solo-ukulele transcription. The remaining perceptual judgment is whether the strums, quiet mouth poses, document readability and new title rhythm feel right in the full trailer. Human headphone/speaker listening approval and exact generated hand fingering are not claimed.\n'
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['status','duration_seconds','frames','encoded_loudness','opening_strum_rms_increase_db','dan_mouth_checks','unplanned_internal_cuts']},indent=2))
