"""Recorded ukulele performance, restrained foley, gradual screen perspective, stereo master."""
from pathlib import Path
from fractions import Fraction
import json,subprocess,hashlib,wave,math,shutil,re
import numpy as np,soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');HERE=ROOT/'trailer/first/finishing-d4'
D3=ROOT/'build/first-trailer-picture-pass-d3';OUT=ROOT/'build/first-trailer-finishing-d4';SAMPLES=HERE/'samples/ukulele/samples';FX=ROOT/'clips/first/finishing-d4/audio'
SR=48000;N=180*SR
for sub in ('stems','speech','score','audio-review'):(OUT/sub).mkdir(parents=True,exist_ok=True)
def read(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar',str(SR),'-f','f32le','-'])
 return np.frombuffer(raw,'<f4').copy()
def write(p,a):sf.write(p,a,SR,subtype='PCM_24')
def add(a,b,t,gain=1):
 i=round(t*SR);n=min(len(b),len(a)-i)
 if n>0:a[i:i+n]+=b[:n]*gain
def peak(a,level):return a*(10**(level/20)/max(np.max(np.abs(a)),1e-8))
def rms(a,level):return a*(10**(level/20)/max(np.sqrt(np.mean(a.astype(float)**2)),1e-8))
def stereo(a,pan=0):
 p=np.asarray(pan);left=np.cos((p+1)*np.pi/4);right=np.sin((p+1)*np.pi/4)
 return np.column_stack([a*left,a*right]).astype(np.float32)
def fade(a,seconds=.025):
 a=a.copy();n=min(round(seconds*SR),len(a)//2);a[:n]*=np.linspace(0,1,n);a[-n:]*=np.linspace(1,0,n);return a
def bed(source,start,end,level):
 a=read(source);a=np.tile(a,math.ceil((end-start)*SR/len(a)))[:round((end-start)*SR)];a=fade(rms(a,level),.20)
 return a
events=json.loads((D3/'score/events.json').read_text());notes=[]
for start in [1,12,16]:
 for j,note in enumerate([57,64,60,64]):
  if start==1 and j==3:continue
  if start==1 and j==2:note=61
  if start+j>=18:continue
  notes.append({'t':start+j,'note':note,'velocity':56,'phrase':start,'beat':j})
# Roy finishes the spoken introduction before he plays. Bass remains half a beat ahead.
for start in [110,114,118,122]:
 for j,note in enumerate([57,64,60,64]):notes.append({'t':start+j,'note':note,'velocity':64,'phrase':start,'beat':j})
sources={57:('C4.flac',60,-5),60:('C4.flac',60,-5),61:('D4.flac',62,-8),64:('E4.flac',64,-2)}
uke=np.zeros(N,np.float32);rendered=[];rng=np.random.default_rng(6266)
for item in notes:
 n=item['note'];filename,root,tune=sources[n];a,sr=sf.read(SAMPLES/filename,dtype='float32');assert sr==48000
 cents=tune+float(rng.uniform(-.6,.6));ratio=2**((n-root)/12+cents/1200);fraction=Fraction(1/ratio).limit_denominator(50000)
 a=resample_poly(a,fraction.numerator,fraction.denominator).astype(np.float32)
 # Shortening release is a player's damping gesture, not a hard sample truncation.
 time=np.arange(len(a))/SR;a*=np.exp(-np.maximum(0,time-.72)/.42)
 target=.037*(item['velocity']/64)*[.96,1.03,.88,1.0][item['beat']]
 a*=target/max(np.sqrt(np.mean(a[:int(.3*SR)].astype(float)**2)),1e-6)
 onset=item['t']+float(rng.uniform(-.014,.014));add(uke,a,onset)
 rendered.append({**item,'actual_onset':onset,'source':filename,'source_root_midi':root,'pitch_ratio':ratio,'tuning_cents':cents,'expected_frequency':440*2**((n-69)/12)})
uke[18*SR:110*SR]=0;uke[int(125.8*SR):126*SR]*=np.linspace(1,0,int(.2*SR));uke[126*SR:]=0
chuck=peak(read(SAMPLES/'chuck.wav'),-39);add(uke,chuck,3.48)
# The sound becomes screen playback as the same moving image pulls back.
screen=sosfilt(butter(2,[185,5300],btype='bandpass',fs=SR,output='sos'),uke).astype(np.float32)
t=np.arange(N,dtype=np.float32)/SR;perspective=np.clip((t-110)/8,0,1);perspective[t<110]=0
uke=uke*(1-perspective)+screen*perspective*.73
pan=-.36*perspective;stems={'ukulele':stereo(uke,pan)}
for name in ('dialogue','piano','bass','strings','brass','percussion'):
 a=read(D3/'stems'/f'{name}.wav');assert len(a)==N
 stems[name]=stereo(a)
# D3's synthetic motor is replaced; preserve the accepted notification exactly.
effects=read(D3/'stems/effects.wav');effects[88*SR:94*SR]=0
motor=fade(peak(read(FX/'shred.mp3'),-21),.06);add(effects,motor,88)
clap=read(FX/'clap.mp3');active=np.flatnonzero(np.abs(clap)>np.max(np.abs(clap))*.08)
clap=clap[max(0,active[0]-240):min(len(clap),active[-1]+int(.18*SR))];add(effects,peak(clap,-25),95.35)
handling=fade(peak(read(FX/'uke_handle.mp3'),-37));add(effects,handling,126.08)
stems['effects']=stereo(effects,-.10)
amb=np.zeros(N,np.float32)
for a,b,level in [(0,18,-54),(18,62,-61),(62,82,-59),(98,104,-61),(104,110,-55),(110,126,-58),(126,148,-60),(148,164,-62),(170,180,-53)]:add(amb,bed(FX/'home.mp3',a,b,level),a)
add(amb,bed(FX/'lodge.mp3',82,98,-47),82)
room=stereo(amb);delay=round(.013*SR);room[:,1]=np.r_[np.zeros(delay),room[:-delay,1]]
stems['ambience']=room
mix=np.zeros((N,2),np.float32)
for name,a in stems.items():
 a[164*SR:166*SR]=0
 if name in ('ukulele','piano','bass','strings','brass','percussion'):a[170*SR:]=0
 write(OUT/'stems'/f'{name}.wav',a);mix+=a
mix[164*SR:166*SR]=0;write(OUT/'premaster.wav',mix)
def loudness(p):
 result=subprocess.run(['ffmpeg','-v','info','-i',str(p),'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 return json.loads(re.findall(r'\{\s*"input_i".*?\}',result.stderr,re.S)[-1])
before=loudness(OUT/'premaster.wav');gain_db=min(12.0,max(-3,-18-float(before['input_i'])))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(OUT/'premaster.wav'),'-af',f'volume={gain_db}dB,aresample=192000,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true,aresample=48000','-c:a','pcm_f32le',str(OUT/'master-limited.wav')],check=True)
master,sr=sf.read(OUT/'master-limited.wav',dtype='float32',always_2d=True);assert sr==SR
master=master[:N];master=np.pad(master,((0,max(0,N-len(master))),(0,0)));master[164*SR:166*SR]=0;write(OUT/'mix.wav',master)
after=loudness(OUT/'mix.wav')
for p in (D3/'speech').glob('*'):shutil.copy2(p,OUT/'speech'/p.name)
for name in ['captions.srt','dialogue.csv','timeline.csv']:shutil.copy2(D3/name,OUT/name)
for p in (D3/'score').iterdir():
 if p.is_file() and not p.name.endswith('-raw.wav'):shutil.copy2(p,OUT/'score'/p.name)
events['events']['ukulele']=[{'t':float(x['t']),'d':.75,'notes':[x['note']],'v':x['velocity']} for x in notes]
(OUT/'score/events.json').write_text(json.dumps(events,indent=2)+'\n')
report={'duration':180,'sample_rate':SR,'channels':2,'samples_per_channel':N,'source':'Recorded Flight Fireball tenor ukulele samples by Mateusz Dąbrowski / FreePats, CC0','source_url':'https://freepats.zenvoid.org/GuitarFamily/ukulele.html','sample_source_tuning':'Published SFZ per-sample cent corrections retained; A3 transposed from C4 by three semitones','performance':'Original motif; natural sample decays, small deterministic timing and velocity variations; no generated music used in master','middle_performance':'First pluck at 110 after Roy’s introduction, last at 125; half-beat bass anticipation retained','notes':rendered,'master_gain_db':gain_db,'premaster_loudness':before,'master_loudness':after,'music_after_170':'exact zero','gate_164_166':'exact zero in master and all stems','dialogue':'Original D3 speech PCM and timings retained; no voice pitch or speed change','new_sound':'Recorded ukulele, screen-perspective filtering and pan, location beds, shredder, tentative clap and handling; original notification retained','credits_used':37,'runway_balance_after_audio_sources':1253}
(OUT/'mix.json').write_text(json.dumps(report,indent=2)+'\n')
for start,duration,name in [(0,18,'opening'),(104,22,'pinterest-reveal'),(148,32,'ending')]:
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-i',str(OUT/'mix.wav'),'-t',str(duration),'-c:a','libmp3lame','-b:a','192k',str(OUT/'audio-review'/(name+'.mp3'))],check=True)
print('Sound complete:',json.dumps(after),'master gain',gain_db,flush=True)
