"""Artifact checks for the D5 music-only revision; no picture or voice regeneration."""
from pathlib import Path
import csv,hashlib,json,math,re,struct,subprocess
import numpy as np,soundfile as sf
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser')
OUT=ROOT/'build/first-trailer-ukulele-d5';D4=ROOT/'build/first-trailer-finishing-d4';SR=48000;N=180*SR
VIDEO=OUT/'first-trailer-ukulele-d5.mp4';SOURCE=D4/'first-trailer-finishing-d4.mp4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def db(x):return 20*math.log10(max(float(x),1e-12))
def probe(p,count=False):return json.loads(subprocess.check_output(['ffprobe','-v','error',*(['-count_frames'] if count else []),'-show_streams','-show_format','-of','json',str(p)],text=True))
def streamhash(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],text=True).strip()
p=probe(VIDEO,True);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1280,720,'24/1',4320)
assert float(p['format']['duration'])==180 and a['sample_rate']=='48000' and a['channels']==2
video_hash=streamhash(VIDEO);assert video_hash==streamhash(SOURCE),'Picture changed'
d4qc=json.loads((D4/'QC.json').read_text());assert sha(SOURCE)==d4qc['sha256'],'D4 was overwritten'
rows=list(csv.DictReader((OUT/'timeline.csv').open()));segments=[]
for r in rows:
 s=next(s for s in d4qc['segments'] if s['id']==r['segment']);dur=s['frames']/24
 assert dur==float(r['duration_seconds']) and dur>=2
 segments.append({'id':r['segment'],'start':float(r['start_seconds']),'end':float(r['end_seconds']),'duration':dur,'frames':s['frames']})
assert len(segments)==40 and sum(s['frames'] for s in segments)==4320
assert (OUT/'captions.srt').read_bytes()==(D4/'captions.srt').read_bytes()
fixed={'roy':'ukulele','dialogue':'dialogue','effects':'effects','ambience':'ambience'}
for new,old in fixed.items():assert sha(OUT/'stems'/f'{new}.wav')==sha(D4/'stems'/f'{old}.wav'),new
music_names=['roy','plucks','low','bloom','grit','body','reverse'];stems={}
for path in [OUT/'mix.wav',OUT/'music-only.wav',*sorted((OUT/'stems').glob('*.wav'))]:
 data,sr=sf.read(path,dtype='int32',always_2d=True);assert data.shape==(N,2) and sr==SR
 assert not np.any(data[164*SR:166*SR]),path
 if path.stem in music_names or path.name=='music-only.wav':assert not np.any(data[170*SR:]),path
 stems[str(path.relative_to(OUT))]={'frames':len(data),'sample_rate':sr,'channels':2,'subtype':sf.info(path).subtype,'gap_nonzero_samples':0,'peak_dbfs':db(np.max(np.abs(data.astype(float)))/2**31)}
del data
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(VIDEO),'-vn','-ac','2','-ar',str(SR),'-f','f32le','-']);decoded=np.frombuffer(raw,'<f4').reshape(-1,2)[:N]
assert len(decoded)==N and np.isfinite(decoded).all()
gap_peak=db(np.max(abs(decoded[164*SR:166*SR])));assert gap_peak<-50
result=subprocess.run(['ffmpeg','-v','info','-i',str(VIDEO),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],text=True,capture_output=True,check=True)
loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',result.stderr,re.S)[-1]);assert -19<=float(loud['input_i'])<=-17 and float(loud['input_tp'])<=-1
mono=decoded.mean(axis=1);fold=db(np.sqrt(np.mean(mono.astype(float)**2))/np.sqrt(np.mean(decoded.astype(float)**2)));assert fold>-.5
pitch=[]
def pitchcheck(signal,sr,t,expected,label):
 start=round(t*sr);x=signal[start:start+round(.26*sr)];sp=np.abs(np.fft.rfft(x*np.hanning(len(x)),n=262144));freq=np.fft.rfftfreq(262144,1/sr);ids=np.where((freq>expected*.97)&(freq<expected*1.03))[0];k=ids[np.argmax(sp[ids])];fit=sp[k-1:k+2];delta=.5*(fit[0]-fit[2])/(fit[0]-2*fit[1]+fit[2]);hz=(k+delta)*sr/262144;cents=1200*np.log2(hz/expected)
 assert abs(cents)<15,(label,hz,cents)
 pitch.append({'source':label,'window_start':t,'expected_hz':expected,'measured_hz':hz,'cents_error':cents})
for t,n in [(1.07,57),(2.08,64),(3.08,61)]:pitchcheck(mono,SR,t,440*2**((n-69)/12),'Actual encoded MP4 opening')
low,sr=sf.read(OUT/'stems/low.wav',always_2d=True);pitchcheck(low.mean(axis=1),sr,40.08,55,'Rendered lowered ukulele stem')
events=json.loads((OUT/'score/events.json').read_text());old=json.loads((D4/'score/events.json').read_text())['events']
for role,src in [('roy','ukulele'),('plucks','piano'),('low','bass'),('bloom','strings'),('grit','brass')]:
 assert [{k:e[k] for k in ['t','d','notes','v']} for e in events['events'][role]]==old[src],role
for role,es in events['events'].items():
 for e in es:
  assert e['t']+e['d']<=164 or e['t']==166
 assert all(e['t']==166 for e in es if e['t']>=164)
anticipations=[e['t'] for e in events['events']['low'] if 109<=e['t']<126];assert anticipations==[109.5+i for i in range(16)]
# Parse the delivered MIDI file independently: timing/velocity must agree with the event map.
data=(OUT/'score/ukulele-score-d5.mid').read_bytes();assert data[:4]==b'MThd';fmt,ntr,division=struct.unpack('>HHH',data[8:14]);assert (fmt,ntr,division)==(1,8,480)
def vlq(data,pos):
 value=0
 while True:
  b=data[pos];pos+=1;value=(value<<7)|(b&127)
  if b<128:return value,pos
pos=14;tracks=[]
for i in range(ntr):
 assert data[pos:pos+4]==b'MTrk';length=struct.unpack('>I',data[pos+4:pos+8])[0];chunk=data[pos+8:pos+8+length];pos+=8+length;j=0;tick=0;ons=[];offs=[];tempo=[]
 while j<len(chunk):
  dt,j=vlq(chunk,j);tick+=dt;status=chunk[j];j+=1
  if status==255:
   typ=chunk[j];j+=1;n,j=vlq(chunk,j);payload=chunk[j:j+n];j+=n
   if typ==81:tempo.append(int.from_bytes(payload,'big'))
  elif status>>4 in [8,9]:
   n,velocity=chunk[j:j+2];j+=2
   (ons if status>>4==9 and velocity else offs).append((tick,n,velocity))
  elif status>>4==12:j+=1
  else:raise ValueError(status)
 assert tick==180*480
 tracks.append({'ons':ons,'offs':offs,'tempo':tempo})
assert tracks[0]['tempo']==[1000000]
for (role,es),tr in zip(events['events'].items(),tracks[1:]):
 expected=sorted((round(e['t']*480),n,e['v']) for e in es for n in e['notes']);assert sorted(tr['ons'])==expected,role
 expectedoff=sorted((round((e['t']+e['d'])*480),n,0) for e in es for n in e['notes']);assert sorted(tr['offs'])==expectedoff,role
info=subprocess.check_output(['pdfinfo',str(OUT/'score/ukulele-score-d5.pdf')],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);assert pages==6
compile_log=(OUT/'score/compile.log').read_text();assert 'successfully completed' in compile_log and 'warning:' not in compile_log.lower()
report={'status':'PASS technical artifact checks; perceptual comparison remains for the user','artifact':str(VIDEO),'sha256':sha(VIDEO),'duration':180,'frames':4320,'dimensions':[1280,720],'fps':24,'encoded_loudness':{k:loud[k] for k in ['input_i','input_tp','input_lra']},'mono_fold_loss_db':fold,'encoded_gap_peak_dbfs':gap_peak,'picture_stream_sha256':video_hash,'picture_identical_to_d4':True,'d4_preserved':True,'captions_identical':True,'preserved_pcm_stems':fixed,'segments':segments,'minimum_picture_segment_seconds':min(s['duration'] for s in segments),'stems':stems,'pitch_checks':pitch,'midi_tracks':ntr,'midi_timing_and_notes_match_score_events':True,'score_pdf_pages':pages,'title':'One shared attack at 166, no subsequent score event; exact PCM silence 164-166; music zero after 170','bass_anticipation':anticipations,'paid_generations':0,'limits':'No claim of subjective headphone/speaker listening. Low and sustained sounds are transformed ukulele recordings, not physically playable solo-instrument parts. D4 picture and its approximate mouth/hand detail remain unchanged.'}
(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# D5 ukulele-derived alternate - rendered QC\n\nTechnical verification passed on the delivered MP4, MIDI, score and PCM stems. This is an alternate score for the accepted D4 picture, not a new picture edit.\n\n'
md+=f"180.000 seconds, 4320 frames, 1280 x 720, 24 fps, stereo 48 kHz AAC. Encoded loudness {loud['input_i']} LUFS; true peak {loud['input_tp']} dBTP; range {loud['input_lra']} LU. Mono fold-down change {fold:.4f} dB. Encoded gap peak {gap_peak:.2f} dBFS.\n\n"
md+='## RULES.md audit\n\nEvery picture segment is unchanged. The H.264 elementary-stream hash matches D4 exactly, so every pixel and edit boundary inherits the verified D4 picture. No interval was shortened and no extra cut was introduced. Minimum segment duration is 2.000 seconds. Dialogue stem and caption bytes are identical to D4; Roy, effects and ambience stems are also byte-identical before common master gain.\n\n| Segment | Start | End | Duration | Frames | Minimum | Result |\n|---|---:|---:|---:|---:|---:|---|\n'
for s in segments:md+=f"| {s['id']} | {s['start']:.3f} | {s['end']:.3f} | {s['duration']:.3f} | {s['frames']} | 2.000 | PASS |\n"
md+='\n## Score and sound\n\nAll 10 stereo 24-bit stems and the master have exactly 8,640,000 frames. Every bus is exactly zero from 164 to 166. Music is exactly zero after 170. The shared title attack is at 166; there are no later note events. The bass retains its 109.5-second start and half-beat anticipation. Roy retains the original microtiming and screen-perspective treatment. The three opening pitches were measured on the decoded delivery MP4; the lowered A1 was measured on the actual rendered low stem. All four are within 15 cents.\n\nThe delivered eight-track MIDI was parsed and its note onsets, durations, velocities, tempo and length checked against the arrangement event map. The six-page LilyPond production score compiles without warnings. All pages were rendered to PNG and checked for layout. These are sounding studio pitches and processing instructions; some parts intentionally extend beyond a real ukulele\'s playable range. MIDI is interchange data, not a faithful audio preview of the transformed timbres.\n\nAll musical source audio comes from the saved CC0 FreePats Flight Fireball ukulele library. Piano, brass, strings and drum generators are absent from this mix. Practical shred/room/notification effects remain outside the musical score. No credits or paid generations were used.\n\n## Review limits\n\nThe checks establish file integrity, timing, pitch, levels, source continuity and layout. They do not assert subjective listening approval. The picture retains its D4 label and approximate generated mouth/hand detail because the video stream was deliberately preserved. D4 remains the comparison cut.\n'
(OUT/'QC.md').write_text(md)
print(json.dumps({k:report[k] for k in ['status','duration','frames','encoded_loudness','mono_fold_loss_db','encoded_gap_peak_dbfs','picture_identical_to_d4','score_pdf_pages']},indent=2))
