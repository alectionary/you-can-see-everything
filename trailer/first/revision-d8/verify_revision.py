"""Verify the actual D8 movie: holds, repeated joke, visible playing, UI and musical timing."""
from pathlib import Path
import csv,json,math,hashlib,re,subprocess,struct
import cv2,numpy as np,soundfile as sf
from scipy.signal import correlate
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-revision-d8';D7=ROOT/'build/first-trailer-revision-d7';VIDEO=OUT/'first-trailer-revision-d8.mp4';SR=48000;N=197*SR
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def db(x):return 20*math.log10(max(float(x),1e-12))
def probe(p,count=False):return json.loads(subprocess.check_output(['ffprobe','-v','error',*(['-count_frames'] if count else []),'-show_streams','-show_format','-of','json',str(p)],text=True))
def frame(p,t):
 c=cv2.VideoCapture(str(p));c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,z=c.read();c.release();assert ok,(p,t);return z
rows=list(csv.DictReader((OUT/'timeline.csv').open()));old={x['segment']:x for x in csv.DictReader((D7/'timeline.csv').open())};p=probe(VIDEO,True);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
assert (int(v['nb_read_frames']),v['r_frame_rate'],v['width'],v['height'])==(4728,'24/1',1280,720)
assert float(p['format']['duration'])==197 and a['sample_rate']=='48000' and a['channels']==2
segments=[];cursor=0
for r in rows:
 q=probe(OUT/'segments'/f"{r['segment']}.mp4")['streams'][0];frames=int(q['nb_frames']);duration=frames/24;expected=float(old[r['segment']]['duration_seconds'])+({'T07':4,'T36':2}.get(r['segment'],0));assert duration>=2 and duration==expected and float(r['start_seconds'])==cursor
 segments.append({'id':r['segment'],'start':cursor,'end':cursor+duration,'duration':duration,'frames':frames});cursor+=duration
assert cursor==197 and len(segments)==44
by={x['id']:x for x in segments};assert by['C01']['end']==by['T17']['start']==82
timing=json.loads((OUT/'speech/timing.json').read_text());lines=list(csv.DictReader((OUT/'dialogue.csv').open()));assert len(timing)==34
for f in (D7/'speech').glob('L*.wav'):assert sha(f)==sha(OUT/'speech'/f.name)
for lid in ['L04r2','L04r3']:assert sha(OUT/'speech'/f'{lid}.wav')==sha(OUT/'speech/L04b.wav')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','2','-ar',str(SR),'-f','f32le','-']);audio=np.frombuffer(raw,'<f4').reshape(-1,2)[:N];mono=audio.mean(axis=1);assert len(audio)==N and np.isfinite(audio).all()
roy,sr=sf.read(OUT/'stems/roy.wav',always_2d=True);assert sr==SR and len(roy)==N
for lo,hi in [(12,18),(112,118),(126,183),(193,197)]:assert not np.any(roy[lo*SR:hi*SR]),(lo,hi)
for role in ['plucks','body']:
 z,sr=sf.read(OUT/'stems'/f'{role}.wav');assert not np.any(z[112*SR:118*SR])
events=json.loads((OUT/'score/events.json').read_text())['events'];motion=json.loads((OUT/'hand-motion.json').read_text());assert sorted(e['t'] for e in events['roy'])==sorted(t for m in motion for t in m['onsets_global'])
premaster,sr=sf.read(OUT/'premaster.wav',always_2d=True);pre=premaster.mean(axis=1);sync=[]
for e in events['roy']:
 t=e['t'];i=round((t-.03)*SR);j=round((t+.16)*SR);pad=round(.04*SR);assert i>=0
 template=pre[i:j].astype(np.float64);actual=mono[i-pad:j+pad].astype(np.float64) if i>=pad else None
 if actual is None:actual=mono[i:j+pad].astype(np.float64);expected=0
 else:expected=pad
 corr=correlate(actual,template,mode='valid',method='fft');lag=(int(np.argmax(corr))-expected)/SR;assert abs(lag)<=1/24,(t,lag)
 stem=db(np.sqrt(np.mean(roy[round(t*SR):round((t+.16)*SR)]**2)));assert stem>-46,(t,stem)
 sync.append({'onset_seconds':t,'audio_lag_in_actual_MP4_seconds':lag,'instrument_attack_rms_dbfs':stem,'motion_source':e['motion_key']})
del premaster,pre
speech=[]
for lid in ['L04a','L04b','L04r2','L04r3','L06','L07','L08','L09','L10','L14','L15','L16','L18','L19','L21','L22','L26','L29','L30']:
 e=next(x for x in timing if x['id']==lid);z,sr=sf.read(OUT/'speech'/f'{lid}.wav');clip=mono[round(e['start']*SR):round(e['start']*SR)+len(z)];c=float(np.corrcoef(clip,z)[0,1]);assert c>.68,(lid,c);speech.append({'id':lid,'speaker':e['speaker'],'start':e['start'],'actual_AAC_source_correlation':c})
replays=[]
for rel in [.1,.6,1.05]:
 pics=[frame(VIDEO,t+rel)[70:540,30:620] for t in [20.25,26.25,30.25]];errors=[float(np.mean(abs(pics[0].astype(float)-p.astype(float)))) for p in pics[1:]];assert max(errors)<4,(rel,errors);replays.append({'relative_to_Dan_assurance_start':rel,'Dan_picture_errors_8bit':errors})
# Actual right panels must be the original reaction and the two independent new performances.
reaction_sources=[(21.3,next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4')),4.4,(0,120,720,900)),(27.3,ROOT/'clips/first/fielder-rehearsal-test-01.mov',3.9,(320,10,960,700)),(31.3,ROOT/'clips/first/picture-pass-d3/fielder_practice.mp4',2.7,(320,10,960,700))]
reaction=[]
from PIL import Image
for global_t,source,source_t,crop in reaction_sources:
 actual=cv2.cvtColor(frame(VIDEO,global_t),cv2.COLOR_BGR2RGB)[44:694,650:1260];candidates=[]
 for dt in [-1/24,0,1/24]:
  z=frame(source,source_t+dt);expected=np.array(Image.fromarray(cv2.cvtColor(z,cv2.COLOR_BGR2RGB)).crop(crop).resize((610,650),Image.Resampling.LANCZOS));candidates.append((float(np.mean(abs(expected[:500].astype(float)-actual[:500].astype(float)))),dt))
 err,dt=min(candidates);assert err<6,(global_t,err);reaction.append({'that_seconds':global_t,'reaction_source':str(source),'reaction_frame_seconds':source_t+dt,'frame_quantization_allowance_seconds':1/24,'actual_right_panel_error_8bit':err})
stable=[]
for n in ['T03','T10','T15','T21']:
 s=by[n];f=frame(VIDEO,s['start']+.3)[60:550,10:1270];g=frame(VIDEO,s['end']-.3)[60:550,10:1270];error=float(np.mean(abs(f.astype(float)-g.astype(float))));assert error<.8,(n,error);stable.append({'segment':n,'card_pixel_change_8bit':error})
moving=[]
for n in ['T12','T13']:
 s=by[n]['start'];f=frame(VIDEO,s+.4);g=frame(VIDEO,s+1.7);live=float(np.mean(abs(f[115:445,330:755].astype(float)-g[115:445,330:755].astype(float))));background=float(np.mean(abs(f[410:680,35:240].astype(float)-g[410:680,35:240].astype(float))));assert live>.8 and background<1.5,(n,live,background);moving.append({'segment':n,'moving_video_difference_8bit':live,'locked_background_difference_8bit':background})
before=frame(VIDEO,131.9);after=frame(VIDEO,133.6);blockdiff=float(np.mean(abs(before[390:540,460:820].astype(float)-after[390:540,460:820].astype(float))));assert blockdiff>3
black=subprocess.check_output(['ffmpeg','-v','error','-ss','177','-i',str(VIDEO),'-t','2','-vf','scale=16:9','-pix_fmt','gray','-f','rawvideo','-']);assert len(black)==48*16*9 and max(black)==0
gate=db(np.max(abs(audio[177*SR:179*SR])));cta=db(np.max(abs(audio[round(193.1*SR):])));assert gate<-50 and cta<-70
r=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1]);assert -19<=float(loud['input_i'])<=-17 and float(loud['input_tp'])<=-1
for lo,hi in [(34,38),(172,174),(174,177)]:assert db(np.sqrt(np.mean(audio[lo*SR:hi*SR]**2)))>-45
pitch=[]
for t,n in [(.20,57),(7.18,61)]:
 hz0=440*2**((n-69)/12);z=mono[round(t*SR):round((t+.15)*SR)];sp=abs(np.fft.rfft(z*np.hanning(len(z)),262144));freq=np.fft.rfftfreq(262144,1/SR);ids=np.where((freq>hz0*.97)&(freq<hz0*1.03))[0];k=ids[np.argmax(sp[ids])];y=sp[k-1:k+2];delta=.5*(y[0]-y[2])/(y[0]-2*y[1]+y[2]);hz=(k+delta)*SR/262144;cents=1200*np.log2(hz/hz0);assert abs(cents)<22,(t,cents);pitch.append({'time':t,'midi':n,'Hz':hz,'cents_error':cents})
data=(OUT/'score/ukulele-score-d8.mid').read_bytes();assert struct.unpack('>HHH',data[8:14])==(1,8,480)
def vlq(d,j):
 value=0
 while True:
  c=d[j];j+=1;value=(value<<7)|(c&127)
  if c<128:return value,j
pos=14;tracks=[]
for tr in range(8):
 assert data[pos:pos+4]==b'MTrk';length=struct.unpack('>I',data[pos+4:pos+8])[0];chunk=data[pos+8:pos+8+length];pos+=8+length;j=0;tick=0;ons=[];offs=[]
 while j<len(chunk):
  dt,j=vlq(chunk,j);tick+=dt;status=chunk[j];j+=1
  if status==255:typ=chunk[j];j+=1;n,j=vlq(chunk,j);j+=n
  elif status>>4 in [8,9]:note,velocity=chunk[j:j+2];j+=2;(ons if status>>4==9 and velocity else offs).append((tick,note,velocity))
  elif status>>4==12:j+=1
  else:raise ValueError(status)
 assert tick==197*480;tracks.append((ons,offs))
for (role,es),(ons,offs) in zip(events.items(),tracks[1:]):
 assert sorted(ons)==sorted((round(e['t']*480),n,e['v']) for e in es for n in e['notes']),role
 assert sorted(offs)==sorted((round((e['t']+e['d'])*480),n,0) for e in es for n in e['notes']),role
info=subprocess.check_output(['pdfinfo',str(OUT/'score/ukulele-score-d8.pdf')],text=True);assert int(re.search(r'Pages:\s+(\d+)',info)[1])==7;log=(OUT/'score/compile.log').read_text();assert 'successfully completed' in log and 'warning:' not in log.lower()
scan=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-an','-vf',"select='gt(scene,0.25)',showinfo",'-f','null','-'],text=True,capture_output=True,check=True);cuts=[float(x) for x in re.findall(r'pts_time:([0-9.]+)',scan.stderr)];allowed=[s['start'] for s in segments]+[34.0];unplanned=[t for t in cuts if min(abs(t-b) for b in allowed)>1.1/24];assert not unplanned,unplanned
report={'status':'PASS encoded technical checks; visual contact-sheet review recorded separately','artifact':str(VIDEO),'sha256':sha(VIDEO),'duration':197,'frames':4728,'segments':segments,'minimum_segment_duration':min(s['duration'] for s in segments),'no_prior_hold_shortened':True,'extensions':{'T07':4,'T36':2},'Dan_identical_audio_replays':True,'Dan_actual_picture_replay_checks':replays,'simultaneous_reaction_source_checks':reaction,'stable_title_checks':stable,'moving_auditions':moving,'block_banner_actual_difference_8bit':blockdiff,'actual_audio_sync_checks':sync,'hand_motion_sources':motion,'accepted_speech_files_preserved':32,'repeated_original_cues':2,'speech_correlations':speech,'silent_Roy_windows':[[12,18],[112,118],[126,183],[193,197]],'encoded_loudness':loud,'encoded_black_gap_peak_dbfs':gate,'CTA_peak_after_AAC_guard_dbfs':cta,'pitch':pitch,'MIDI_matches_events':True,'score_pages':7,'scene_changes':cuts,'unplanned_internal_cuts':unplanned,'Pinterest_handle':'@YOU_CAN_SEE_EVERYTHING','new_Runway_generations':0,'new_voice_generations':0,'new_images':3,'limits':'Motion peaks plus sampled visual review align string attacks and exclude idle/hand-opening gestures. Generated fingerings and exact musical pitches are not mechanically exact. No subjective headphone/speaker listening approval is claimed.'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n');md='# D8 final encoded QC\n\n197.000 seconds, 4,728 frames, 1280 × 720, 24 fps, stereo AAC 48 kHz.\n\n## RULES.md audit\n\nAll 44 prior holds retain or extend their durations. T07 adds four seconds for replay plus follow-up; T36 adds two for the billboard reveal. Minimum is 2.000 seconds. No interval is shortened to fund another. The user explicitly requested new title cards over existing spoken audio and two replays of the original Dan line; those requests supersede the older teaser dialogue/card restrictions. All 32 accepted speech files remain byte-identical, with two copies of the same Dan assurance added. Final export is decoded and scene-scanned.\n\n| Segment | Start | End | Actual duration | Frames | Result |\n|---|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | PASS ≥2.000 |\n"
md+=f"\n## Actual artifact checks\n\nEncoded loudness {loud['input_i']} LUFS, true peak {loud['input_tp']} dBTP. Original Dan assurance audio files are identical; decoded export correlations and repeated left-panel frame comparisons confirm the same playback in all three takes. The right panels match the original reaction and two distinct practice sources at the planned 'that' anchors. Requested static cards measure stable pixels; audition inserts show moving video on a locked MacBook background. The actual block banner appears at the end of the second DM exchange. Every clean Roy attack matches a reviewed source-hand event and the actual encoded soundtrack timing within one video frame. The clean strum stem is exactly silent during 12–18 and Roy's non-playing 112–118 introduction. The extended rehearsal and billboard beats contain music. Black/silence is 177–179; one ensemble title attack at 179; transformed score stops at 183; room ukulele ends at 193; CTA 193–197 is silent. MIDI is independently parsed and matches all exact event onsets/offsets through 197 seconds. Seven score pages compile without warnings.\n\n"
md+='Visual review covers the fifteen requested edits, readable DMs and captions, original simultaneous reaction, independent practice takes, stable cards, friendly plan, absurd angry reaction count, Nathan post reveal and Roy/lawyer DM-to-Times-Square pullback. The corresponding actual-output contact sheets are saved in contacts/. See EDIT_NOTES.md for the per-request checklist. These checks do not certify exact generated fingering or subjective headphone/speaker listening.\n';(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['status','duration','frames','minimum_segment_duration','Dan_actual_picture_replay_checks','stable_title_checks','moving_auditions','encoded_loudness','unplanned_internal_cuts']},indent=2))
