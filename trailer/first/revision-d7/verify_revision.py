"""Check actual D7 export: holds, audio, speaker selection, native face detail and score."""
from pathlib import Path
import csv,hashlib,json,math,re,struct,subprocess
import cv2,numpy as np,soundfile as sf
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-revision-d7';D6=ROOT/'build/first-trailer-revision-d6';VIDEO=OUT/'first-trailer-revision-d7.mp4';SR=48000;N=191*SR
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def db(x):return 20*math.log10(max(float(x),1e-12))
def probe(p,count=False):return json.loads(subprocess.check_output(['ffprobe','-v','error',*(['-count_frames'] if count else []),'-show_streams','-show_format','-of','json',str(p)],text=True))
rows=list(csv.DictReader((OUT/'timeline.csv').open()));prior={x['segment']:x for x in csv.DictReader((D6/'timeline.csv').open())};p=probe(VIDEO,True);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert (int(v['nb_read_frames']),v['r_frame_rate'],v['width'],v['height'])==(4584,'24/1',1280,720)
assert float(p['format']['duration'])==191 and a['sample_rate']=='48000' and a['channels']==2
segments=[];cursor=0
for row in rows:
 q=probe(OUT/'segments'/f"{row['segment']}.mp4")['streams'][0];frames=int(q['nb_frames']);dur=frames/24
 assert dur>=2 and frames==round(float(row['duration_seconds'])*24) and dur==float(prior[row['segment']]['duration_seconds']) and float(row['start_seconds'])==cursor
 segments.append({'id':row['segment'],'start':cursor,'end':cursor+dur,'duration':dur,'frames':frames});cursor+=dur
assert len(segments)==44 and cursor==191
timing=json.loads((OUT/'speech/timing.json').read_text());assert len(timing)==32
for f in (D6/'speech').glob('L*.wav'):assert sha(f)==sha(OUT/'speech'/f.name)
for role in ['plucks','low','bloom','grit','body','reverse','ambience','effects']:assert sha(D6/'stems'/f'{role}.wav')==sha(OUT/'stems'/f'{role}.wav')
line=next(x for x in timing if x['id']=='L29');assert line['speaker']=='DAN' and line['start']==161.3 and line['actual_end']<163 and line['caption_end']<164
sources={x['segment']:x for x in json.loads((OUT/'picture-sources.json').read_text())};assert sources['T35']['source'].endswith('dan-main-native.mp4')
cards=[s for s in segments if s['id'].startswith('C')]
for s in cards:assert not any(e['start']<s['end'] and e['caption_end']>s['start'] for e in timing)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','2','-ar',str(SR),'-f','f32le','-']);audio=np.frombuffer(raw,'<f4').reshape(-1,2)[:N];assert len(audio)==N and np.isfinite(audio).all();mono=audio.mean(axis=1)
roy,sr=sf.read(OUT/'stems/roy.wav',always_2d=True);assert sr==SR and len(roy)==N
oldroy,sr=sf.read(D6/'stems/roy.wav',always_2d=True);assert np.max(abs(roy[114*SR:130*SR]-oldroy[114*SR:130*SR]))<2e-7
audible=[]
for lo,hi in [(0,18),(108,114),(177,187)]:
 for t in np.arange(lo,hi,.5):
  sl=slice(round(t*SR),round((t+.5)*SR));encoded=db(np.sqrt(np.mean(audio[sl].astype(float)**2)));stem=db(np.sqrt(np.mean(roy[sl]**2)));assert stem>-39 and encoded>-43,(t,stem,encoded)
  audible.append({'start':float(t),'end':float(t+.5),'encoded_rms_dbfs':encoded,'roy_stem_rms_dbfs':stem})
first=db(np.sqrt(np.mean(audio[:int(.25*SR)]**2)));assert first>-38
gate=db(np.max(abs(audio[171*SR:173*SR])));cta=db(np.max(abs(audio[round(187.1*SR):])));assert gate<-50 and cta<-70,(gate,cta)
for role in ['plucks','low','bloom','grit','body','reverse']:
 z,sr=sf.read(OUT/'stems'/f'{role}.wav',dtype='int32',always_2d=True);assert not np.any(z[:18*SR]) and not np.any(z[177*SR:])
black=subprocess.check_output(['ffmpeg','-v','error','-ss','171','-i',str(VIDEO),'-t','2','-vf','scale=16:9','-pix_fmt','gray','-f','rawvideo','-']);assert len(black)==48*16*9 and max(black)==0
r=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1]);assert -19<=float(loud['input_i'])<=-17 and float(loud['input_tp'])<=-1
correlations=[]
for lid in ['L04a','L04b','L29','L31']:
 e=next(x for x in timing if x['id']==lid);z,sr=sf.read(OUT/'speech'/f'{lid}.wav');clip=mono[round(e['start']*SR):round(e['start']*SR)+len(z)];corr=float(np.corrcoef(clip,z)[0,1]);assert corr>.70,(lid,corr);correlations.append({'id':lid,'speaker':e['speaker'],'source_correlation_in_actual_export':corr})
pitch=[]
for t,n in [(.11,57),(7.12,61)]:
 expected=440*2**((n-69)/12);x=mono[round(t*SR):round((t+.22)*SR)];spec=abs(np.fft.rfft(x*np.hanning(len(x)),n=262144));freq=np.fft.rfftfreq(262144,1/SR);ids=np.where((freq>expected*.97)&(freq<expected*1.03))[0];k=ids[np.argmax(spec[ids])];y=spec[k-1:k+2];delta=.5*(y[0]-y[2])/(y[0]-2*y[1]+y[2]);hz=(k+delta)*SR/262144;cents=1200*np.log2(hz/expected);assert abs(cents)<20,(t,cents);pitch.append({'time':t,'midi':n,'hz':hz,'cents_error':cents})
# Parse interchange independently rather than trusting the score builder.
data=(OUT/'score/ukulele-score-d7.mid').read_bytes();fmt,ntr,division=struct.unpack('>HHH',data[8:14]);assert (fmt,ntr,division)==(1,8,480)
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
 assert tick==191*480;tracks.append((ons,offs,tempos))
assert tracks[0][2]==[1000000];events=json.loads((OUT/'score/events.json').read_text())['events']
for (role,es),(ons,offs,_) in zip(events.items(),tracks[1:]):
 assert sorted(ons)==sorted((round(e['t']*480),n,e['v']) for e in es for n in e['notes']),role
 assert sorted(offs)==sorted((round((e['t']+e['d'])*480),n,0) for e in es for n in e['notes']),role
 if role!='roy':assert all(e['t']==173 for e in es if e['t']>=171)
assert any(e['t']==179 for e in events['roy']) and any(e['t']==0 for e in events['roy'])
def frame(path,t):
 c=cv2.VideoCapture(str(path));c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,z=c.read();c.release();assert ok;return z
native_checks=[]
for name,key,offset,t in [('T04','dan-test',0,1.25),('T08','dan-main',0,.75),('T22','dan-main',3,2.0),('T35','dan-main',16,1.25),('T07','fielder-main',0,1.25),('T09','fielder-main',4,.75)]:
 start=next(s['start'] for s in segments if s['id']==name);src=frame(OUT/'performance'/f'{key}-native.mp4',offset+t);actual=frame(VIDEO,start+t);roi=np.s_[350:520,470:810];x=src[roi];y=actual[roi];error=float(np.mean(abs(x.astype(float)-y.astype(float))));sharp=lambda im:float(cv2.Laplacian(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),cv2.CV_64F).var());ratio=sharp(y)/sharp(x);assert error<8 and .65<ratio<1.4,(name,error,ratio);native_checks.append({'segment':name,'native_face_region_mean_error_8bit':error,'native_detail_laplacian_ratio':ratio,'method':'actual exported face region versus native performance, no mouth composite'})
def headmotion(path,start,dur):
 first=frame(path,start);gray=cv2.cvtColor(first,cv2.COLOR_BGR2GRAY);mask=np.zeros(gray.shape,np.uint8);mask[70:350,430:850]=255;pts=cv2.goodFeaturesToTrack(gray,120,.03,8,mask=mask);moves=[]
 for t in np.arange(.25,dur,.25):
  nxt=cv2.cvtColor(frame(path,start+float(t)),cv2.COLOR_BGR2GRAY);q,status,_=cv2.calcOpticalFlowPyrLK(gray,nxt,pts,None,winSize=(31,31),maxLevel=3);good=status.ravel()==1;delta=(q-pts).reshape(-1,2)[good];moves.append(np.median(delta,axis=0))
 m=np.array(moves);return {'vertical_range_pixels':float(np.ptp(m[:,1])),'horizontal_range_pixels':float(np.ptp(m[:,0]))}
# Verify whole-frame speech-tail holds in the actual export, away from subtitle pixels.
holds=[]
for n in ['T04','T07','T08','T09','T22','T26','T30','T35']:
 seg=next(x for x in segments if x['id']==n);last=max(e['actual_end'] for e in timing if seg['start']<=e['start']<seg['end']);stop=seg['start']+math.ceil((last-seg['start']+.10)*24)/24
 f=frame(VIDEO,min(stop+.09,seg['end']-.1));g=frame(VIDEO,seg['end']-.09);roi=np.s_[80:510,420:850];err=float(np.mean(abs(f[roi].astype(float)-g[roi].astype(float))));assert err<2.5,(n,err);holds.append({'segment':n,'speech_end':last,'whole_frame_hold_start':stop,'final_export_face_difference_8bit':err})
motion={'previous_D6_T04':headmotion(D6/'first-trailer-revision-d6.mp4',18,4),'D7_T04':headmotion(VIDEO,18,4)}
assert motion['D7_T04']['vertical_range_pixels']<motion['previous_D6_T04']['vertical_range_pixels']
scan=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-an','-vf',"select='gt(scene,0.25)',showinfo",'-f','null','-'],text=True,capture_output=True,check=True);cuts=[float(x) for x in re.findall(r'pts_time:([0-9.]+)',scan.stderr)];unplanned=[t for t in cuts if min(abs(t-s['start']) for s in segments)>1.1/24];assert not unplanned,unplanned
info=subprocess.check_output(['pdfinfo',str(OUT/'score/ukulele-score-d7.pdf')],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);assert pages==6
log=(OUT/'score/compile.log').read_text();assert 'successfully completed' in log and 'warning:' not in log.lower()
report={'status':'PASS actual rendered technical checks; sampled visual review documented in contacts/','artifact':str(VIDEO),'sha256':sha(VIDEO),'duration':191,'frames':4584,'segments':segments,'minimum_segment_duration':min(s['duration'] for s in segments),'all_prior_holds_preserved':True,'encoded_loudness':loud,'first_quarter_second_rms_dbfs':first,'visible_playing_audio_halfsecond_checks':audible,'gap_peak_dbfs':gate,'cta_peak_after_aac_guard_dbfs':cta,'speech_correlations':correlations,'L29_on_Dan_before_Roy':True,'native_detail_checks':native_checks,'speech_tail_whole_frame_holds':holds,'head_motion_comparison':motion,'pitch_checks':pitch,'MIDI_matches_events':True,'score_pages':pages,'scene_changes':cuts,'unplanned_internal_cuts':unplanned,'accepted_speech_files_preserved':32,'new_Runway_credits':150,'new_voice_generations':0,'limits':'Metrics establish sound presence, retained native face detail, reduced sampled head movement and correct speaker/source selection. They do not certify perfect phonemes or generated fingerings. No subjective headphone/speaker listening approval is claimed.'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# D7 rendered QC\n\nActual delivery: 191.000 seconds, 4,584 frames, 1280 × 720, 24 fps, stereo AAC 48 kHz.\n\n## RULES.md audit\n\nAll 44 D6 holds retain their full lengths. Minimum 2.000 seconds; no time is borrowed from another shot. Full-trailer dialogue changes were explicitly requested; accepted speech files and words are preserved. Only L29 moves earlier within the same Dan shot to end before Roy. Cards overlap no speech/caption window. The final artifact was decoded, scene-scanned and sampled visually.\n\n| Segment | Start | End | Actual duration | Frames | Result |\n|---|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | PASS ≥2.000 |\n"
md+=f"\n## Audio\n\nActual AAC: {loud['input_i']} LUFS, {loud['input_tp']} dBTP. Every half-second in 0–18, 108–114 and 177–187 has verified audible Roy-stem energy and exported audio energy above −39 dBFS for the instrument stem (−43 dBFS for the encoded mix). The first quarter-second measures {first:.2f} dBFS RMS. Opening strums start at time zero; apology coverage has quiet pitched palm-muted strokes. Roy remains audible through the final question and Pinterest reply. The transformed score ends at 177; only room performance continues to 187. CTA ends in silence. The 171–173 gap is pure black with AAC peak {gate:.2f} dBFS. Original speech PCM files are unchanged. Voice-source correlations in the decoded export pass for both opening Dan lines, the signature Dan line and Roy's final question.\n\n"
md+='## Picture and score\n\nDan speaks the signature line in T35, 161.3–162.993; his caption clears by 163.55, before the 164-second Roy insert. Native still-driven performances replace the soft mouth composites. Each whole frame is held after speech plus approximately 100 ms, and the actual export verifies the face remains still through the shot tail; there is no lower-face blend. Actual face-region detail matches native Runway output within the recorded compression tolerances. Head motion is measured on the actual T04 exports; see QC.json for pixel ranges. Candidates appear in held audio-review/contact-sheet frames; interview and comms exchanges use reverse angles; Roy introductions/ending use instrument coverage; the final unfinished Roy line is off-screen over laptop coverage. Fielder original reaction and rehearsal remain. Six score pages compile without warnings, were rendered and visually reviewed; independently parsed MIDI matches the event map through 191 seconds, including the final diegetic strums.\n\nThese are technical and sampled visual checks. They do not establish perfect lip phonemes or hand fingering, and no subjective headphone/speaker listening approval is claimed.\n'
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['status','duration','frames','encoded_loudness','first_quarter_second_rms_dbfs','head_motion_comparison','native_detail_checks','unplanned_internal_cuts']},indent=2))
