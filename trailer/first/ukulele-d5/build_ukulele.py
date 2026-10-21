"""D5 ukulele-derived alternate. Reuses D4 picture/dialogue without regenerating either."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import csv, hashlib, json, math, re, shutil, struct, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser')
D4=ROOT/'build/first-trailer-finishing-d4'
OUT=ROOT/'build/first-trailer-ukulele-d5'
HERE=ROOT/'trailer/first/ukulele-d5'
SAMPLES=ROOT/'trailer/first/finishing-d4/samples/ukulele/samples'
SR=48000; N=180*SR
ROLES={
 'roy':('Roy - clean ukulele','Roy','treble','ukulele'),
 'plucks':('Uke - displaced motif','Pluck','treble','piano'),
 'low':('Uke - lowered pulse','Low','bass','bass'),
 'bloom':('Uke - stretched resonance','Bloom','treble','strings'),
 'grit':('Uke - distorted cluster','Grit','bass','brass'),
 'body':('Uke - body / muted strum','Body','percussion','percussion'),
 'reverse':('Uke - reversed breath','Rev.','treble',None),
}
EVENTFILE=OUT/'score/events.json'
def ff(args,**kw):return subprocess.run(['ffmpeg','-hide_banner','-y',*map(str,args)],check=True,**kw)
def put(p,v):p.write_text(json.dumps(v,indent=2,default=lambda x:x.item())+'\n')
def read(p):
 a,sr=sf.read(p,dtype='float32',always_2d=True);assert sr==SR
 return a
def save(p,a):sf.write(p,np.asarray(a,dtype=np.float32),SR,subtype='PCM_24')
def mono(p):return read(p).mean(axis=1)
def add(a,b,t,g=1):
 i=round(t*SR);start=max(0,-i);i=max(i,0);n=min(len(b)-start,len(a)-i)
 if n>0:a[i:i+n]+=b[start:start+n]*g
def stereo(a,pan=0):
 return np.column_stack((a*np.cos((pan+1)*np.pi/4),a*np.sin((pan+1)*np.pi/4))).astype(np.float32)
def envelope(a,attack=.008,release=.08):
 a=a.copy();n=min(int(attack*SR),len(a)//2);m=min(int(release*SR),len(a)//2)
 if n:a[:n]*=np.sin(np.linspace(0,np.pi/2,n))**2
 if m:a[-m:]*=np.cos(np.linspace(0,np.pi/2,m))**2
 return a
def norm(a):
 return a/max(np.sqrt(np.mean(a[:min(len(a),int(.3*SR))].astype(float)**2)),1e-7)
def filt(a,lo=None,hi=None):
 if lo and hi:sos=butter(2,[lo,hi],btype='bandpass',fs=SR,output='sos')
 elif lo:sos=butter(2,lo,btype='highpass',fs=SR,output='sos')
 else:sos=butter(2,hi,btype='lowpass',fs=SR,output='sos')
 return sosfilt(sos,a).astype(np.float32)
def echo(a,delays=((.113,.13),(.227,.07))):
 b=a.copy()
 for delay,g in delays:
  k=round(delay*SR)
  if k<len(a):b[k:]+=a[:-k]*g
 return b
def init():
 for d in [OUT,OUT/'score',OUT/'stems',OUT/'audio-review',OUT/'pdf-review',HERE]:d.mkdir(parents=True,exist_ok=True)
def compose():
 init();old=json.loads((D4/'score/events.json').read_text())['events'];events={}
 for role,(_,_,_,source) in ROLES.items():
  events[role]=[dict(e,source_staff=source,source_event=i) for i,e in enumerate(old[source])] if source else []
 # These swells arrive at structural turns; pitches remain from Roy's phrase.
 for end,d,n in [(40,1.25,64),(62,1.25,60),(82,1.5,57),(98,1,64),(126,1.5,64),(148,2,60),(160,1.5,57),(164,1.5,58)]:
  events['reverse'].append({'t':end-d,'d':d,'notes':[n],'v':44+int(end*.24),'source_staff':'new transition','arrival':end})
 # Body percussion is not a pitched kick drum. MIDI 47/48 name the SFZ articulations.
 for i,e in enumerate(events['body']):e['notes']=[47 if i%3==0 else 48]
 report={'version':'D5 alternate','tempo_quarter':60,'meter':'4/4','duration_seconds':180,
  'timing':'One quarter note is one second. JSON drives notation, MIDI and transformed audio. Roy retains D4 microtiming.',
  'notation':'Sounding output pitches; low and sustained parts are studio transformations, not a playable solo-ukulele transcription.',
  'roles':{k:{'name':v[0],'source_staff':v[3]} for k,v in ROLES.items()},'events':events,
  'processing':{'roy':'D4 clean recorded performance, byte-identical stem; screen perspective retained',
  'plucks':'Recorded notes; dry -> subtle detuned double / short echoes / saturation',
  'low':'C4 recording resampled down to original bass pitches; low-pass and parallel saturation',
  'bloom':'Recorded notes phase-vocoder stretched at unchanged pitch; soft swells and growing tremolo',
  'grit':'Recorded low chord, stretched and driven through tanh; no brass sample',
  'body':'Recorded body-tap and muted-strum articulations; no synthesized drum or shredder in music',
  'reverse':'Recorded pluck reversed into the next structural cue'},
  'title':'All title-note events begin exactly at 166; one attack, no retrigger; decay ends by 170',
  'gates':[[164,166],[170,180]],'paid_generations':0}
 put(EVENTFILE,report)
 for name in ['timeline.csv','captions.srt','dialogue.csv']:shutil.copy2(D4/name,OUT/name)
 print('Composed', {k:len(v) for k,v in events.items()},flush=True)

def vlq(n):
 a=[n&127];n>>=7
 while n:a.insert(0,(n&127)|128);n>>=7
 return bytes(a)
def track(messages):
 data=b'';last=0
 for tick,priority,msg in sorted(messages,key=lambda x:(x[0],x[1])):data+=vlq(tick-last)+msg;last=tick
 data+=vlq(180*480-last)+b'\xff\x2f\x00'
 return b'MTrk'+struct.pack('>I',len(data))+data
def midi(events):
 conductor=track([(0,0,b'\xff\x51\x03\x0f\x42\x40'),(0,1,b'\xff\x58\x04\x04\x02\x18\x08')])
 tracks=[conductor]
 for channel,(role,ev) in enumerate(events.items()):
  name=ROLES[role][0].encode();messages=[(0,0,b'\xff\x03'+vlq(len(name))+name),(0,1,bytes([0xc0+channel,24]))]
  for e in ev:
   for n in e['notes']:
    messages.extend([(round(e['t']*480),3,bytes([0x90+channel,n,e['v']])),(round((e['t']+e['d'])*480),2,bytes([0x80+channel,n,0]))])
  tr=track(messages);tracks.append(tr)
  (OUT/'score'/f'{role}.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+tr)
 (OUT/'score/ukulele-score-d5.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(tracks),480)+b''.join(tracks))
def pitch(n):
 names=['c','cis','d','ees','e','f','fis','g','aes','a','bes','b'];octave=n//12-4
 return names[n%12]+("'"*octave if octave>=0 else ','*(-octave))
def notation(events,body=False):
 out=[];last_dyn=''
 for bar in range(45):
  a=bar*4;b=a+4;es=[e for e in events if e['t']<b and e['t']+e['d']>a]
  points=sorted({a,b,*[max(a,e['t']) for e in es],*[min(b,e['t']+e['d']) for e in es]})
  for lo,hi in zip(points,points[1:]):
   e=next((e for e in es if e['t']<=lo<e['t']+e['d']),None);ticks=round((hi-lo)*4);cursor=lo
   while ticks:
    size=next(x for x in [16,8,4,2,1] if x<=ticks);dur={16:'1',8:'2',4:'4',2:'8',1:'16'}[size]
    note='r' if e is None else ("c'" if body else '<'+' '.join(pitch(n) for n in e['notes'])+'>')
    dyn='' if e is None or cursor!=e['t'] else ('\\pp' if e['v']<50 else '\\p' if e['v']<70 else '\\mf' if e['v']<90 else '\\f' if e['v']<110 else '\\ff')
    if dyn==last_dyn:dyn=''
    elif dyn:last_dyn=dyn
    if e and body and e['notes'][0]==48:note="\\once \\override NoteHead.style = #'cross "+note
    tie='~' if e and cursor+size/4<e['t']+e['d'] else ''
    out.append(note+dur+dyn+tie);cursor+=size/4;ticks-=size
  out.append('|\n')
 return ' '.join(out)
def score():
 init();data=json.loads(EVENTFILE.read_text());events=data['events'];midi(events)
 cues={0:'Roy alone',18:'Rehearsal',40:'Casting',62:'Corporate review',82:'Publicity',104:'Stream intro',110:'Roy plays',126:'Authenticity',148:'Fracture',164:'Silence / title at 2:46',170:'Room only'}
 glob='\\numericTimeSignature \\time 4/4 \\tempo 4 = 60 \\key a \\minor\n'
 for t in range(180):
  if t in cues:glob+=f'\\mark \\markup \\small "{t//60}:{t%60:02d} {cues[t]}" '
  glob+='s4 '
  if (t+1)%4==0:glob+='|\n'
  if (t+1)%32==0:glob+='\\pageBreak '
  elif (t+1)%16==0 and t+1<176:glob+='\\break '
 s='''\\version "2.24.3"
#(set-global-staff-size 15)
\\header { title = "YOU CAN SEE EVERYTHING" subtitle = "D5 - a score made entirely from ukulele recordings" subsubtitle = "180 seconds | quarter = 60 | sounding studio pitches" composer = "Original trailer arrangement" tagline = ##f }
\\paper { #(set-paper-size "a3") indent = 39\\mm short-indent = 14\\mm top-margin = 12\\mm bottom-margin = 12\\mm system-system-spacing.basic-distance = #25 }
'''
 s+='global = { '+glob+' }\n'
 for role,ev in events.items():s+=role+'Music = \\absolute { '+notation(ev,role=='body')+' }\n'
 s+='\\markup \\column { \\small "A-E-C-E passes from Roy to displaced plucks, stretched resonance and low pulses. Each 4/4 bar lasts four seconds." \\small "Low pitches, sustains, reversal and distortion are sample processing; these are not solo-instrument fingerings." \\small "Body staff: round note = body tap; cross note = muted strum. MIDI is timing interchange, not the finished timbre." \\small "Roy retains D4 microtiming; all other onsets follow this grid. Silence at 2:44; one attack at 2:46; no music after 2:50." }\n'
 s+='\\score { <<\n'
 for role,(name,short,clef,_) in ROLES.items():
  extra=' \\override StaffSymbol.line-count = #1' if role=='body' else ''
  s+=f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}"{extra} }} << \\global {{ \\clef {clef} \\{role}Music }} >>\n'
 s+='>> \\layout { \\context { \\Score \\override RehearsalMark.self-alignment-X = #LEFT } } }\n'
 p=OUT/'score/ukulele-score-d5.ly';p.write_text(s)
 result=subprocess.run(['lilypond','-dno-point-and-click','-o',str(p.with_suffix('')),str(p)],capture_output=True,text=True)
 (OUT/'score/compile.log').write_text(result.stdout+result.stderr)
 if result.returncode:raise RuntimeError(result.stderr)
 print('Score PDF and 8-track MIDI written',flush=True)

# The actual sound source is the CC0 Flight Fireball tenor ukulele sample set.
ROOTS={60:('C4.flac',-5),62:('D4.flac',-8),64:('E4.flac',-2),66:('F#4.flac',-11),67:('G4.flac',-1),69:('A4.flac',0),71:('B4.flac',0),73:('C#5.flac',0),75:('D#5.flac',3),77:('F5.flac',4),79:('G5.flac',6),81:('A5.flac',8),84:('C6.flac',4)}
@lru_cache(maxsize=64)
def sample(note,detune=0):
 root=min(ROOTS,key=lambda n:abs(n-note));file,tune=ROOTS[root];a=mono(SAMPLES/file)
 ratio=2**((note-root)/12+(tune+detune)/1200);fraction=Fraction(1/ratio).limit_denominator(20000)
 return resample_poly(a,fraction.numerator,fraction.denominator).astype(np.float32)
@lru_cache(maxsize=40)
def stretch(note):
 import librosa
 a=sample(note);a=librosa.effects.time_stretch(a,rate=.22)
 return a.astype(np.float32)
def dur_audio(a,seconds):
 n=round(seconds*SR);return np.pad(a[:n],(0,max(0,n-len(a))))
def render_voice(role,e):
 d=e['d'];at=e['t'];progress=np.clip((at-18)/146,0,1);v=(e['v']/90)**1.25
 if role=='plucks':
  length=4 if at==166 else min(2,d+.85);a=np.zeros(round(length*SR),np.float32)
  for n in e['notes']:
   z=dur_audio(sample(n),length);z*=np.exp(-np.arange(len(z))/SR/(1.2 if at==166 else .62));a+=z/max(1,len(e['notes'])**.65)
   if at>=40:
    detuned=dur_audio(sample(n,5+progress*5),length);detuned*=np.exp(-np.arange(len(detuned))/SR/.68)
    a+=detuned*.12/max(1,len(e['notes'])**.65)
  a=echo(a);a=np.tanh(a*(1+progress*.7))/(1+progress*.7)
  return envelope(norm(a)*v,.003,.08)
 if role=='low':
  length=4 if at==166 else min(1.25,d+.25);a=dur_audio(sample(e['notes'][0]),length)
  a=filt(a,lo=30,hi=700);a=norm(a);a=.7*a+.3*np.tanh(a*2)/2
  a*=np.exp(-np.arange(len(a))/SR/(1.0 if at==166 else .36))
  return envelope(a*v,.012,.04)
 if role in ['bloom','grit']:
  a=np.zeros(round(d*SR),np.float32)
  for n in e['notes']:
   z=dur_audio(stretch(n),d);z=norm(z);a+=z/max(1,len(e['notes'])**.7)
  x=np.arange(len(a),dtype=np.float32)/SR
  if role=='bloom':
   a=filt(a,lo=180,hi=4200);a*=1-(.10+.18*progress)*(1+np.sin(2*np.pi*(2+4*progress)*x))*.5
   a=echo(a,((.071,.10),(.143,.08)))
  else:
   a=filt(a,lo=38,hi=2100);a=np.tanh(a*(1.5+progress*2.5));a=filt(a,hi=2500)
  if at==166:a*=np.exp(-x/1.05)
  return envelope(a*v,.012 if at==166 else (.35 if role=='bloom' else .07),.15)
 if role=='body':
  a=mono(SAMPLES/('body-tap.flac' if e['notes'][0]==47 else 'chuck.wav'))
  if at>=126:
   f=Fraction(1/.8).limit_denominator(100);a=resample_poly(a,f.numerator,f.denominator).astype(np.float32)
  a=filt(a,lo=70,hi=5200);a=echo(a,((.085,.08),))
  return envelope(norm(a)*v,.002,.025)
 if role=='reverse':
  a=dur_audio(sample(e['notes'][0]),d)[::-1].copy();return envelope(norm(a)*v,.10,.025)
 raise ValueError(role)

def loudness(p):
 r=ff(['-v','info','-i',p,'-af','loudnorm=I=-18:TP=-1.2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
 return json.loads(re.findall(r'\{\s*"input_i".*?\}',r.stderr,re.S)[-1])
def audio():
 init();data=json.loads(EVENTFILE.read_text());timing=json.loads((D4/'speech/timing.json').read_text());duck=np.ones(N,np.float32)
 # Smooth ducking follows the real accepted voice lengths, including the two corrected Fielder cues.
 for line in timing:
  lo=max(0,round((line['start']-.07)*SR));hi=min(N,round((line['actual_end']+.13)*SR));duck[lo:hi]=.28
 grid=np.arange(0,N,240);coarse=duck[grid]
 for _ in range(4):coarse=np.convolve(coarse,[.2,.6,.2],mode='same')
 duck=np.interp(np.arange(N),grid,coarse).astype(np.float32)
 music=np.zeros((N,2),np.float32);gain_report={};stems={}
 pans={'plucks':-.12,'low':0,'bloom':.12,'grit':-.08,'body':.14,'reverse':-.18}
 matches={'plucks':('piano',1.12),'low':('bass',.90),'bloom':('strings',.82),'grit':('brass',.78),'body':('percussion',.95)}
 for role,ev in data['events'].items():
  if role=='roy':
   dest=OUT/'stems/roy.wav';shutil.copy2(D4/'stems/ukulele.wav',dest);a=read(dest);music+=a;stems[role]=str(dest);continue
  mono_bus=np.zeros(N,np.float32)
  for e in ev:add(mono_bus,render_voice(role,e),e['t'])
  mono_bus*=duck
  # Return the phrase to Roy's hands at the stream entry, then let the derived layers re-enter.
  if role in ['plucks','bloom','body','grit']:
   t=np.arange(N,dtype=np.float32)/SR;factor=np.ones(N,np.float32);mask=(t>=110)&(t<118);factor[mask]=.15+.85*(t[mask]-110)/8;mono_bus*=factor
  a=stereo(mono_bus,pans[role]);a[164*SR:166*SR]=0;a[170*SR:]=0
  a[round(163.95*SR):164*SR]*=np.linspace(1,0,int(.05*SR))[:,None]
  a[round(169.9*SR):170*SR]*=np.linspace(1,0,int(.1*SR))[:,None]
  if role in matches:
   original,ratio=matches[role];ref=read(D4/'stems'/f'{original}.wav');rms_ref=np.sqrt(np.mean(ref[18*SR:164*SR].astype(float)**2));rms_new=np.sqrt(np.mean(a[18*SR:164*SR].astype(float)**2));g=rms_ref*ratio/max(rms_new,1e-9)
  else:g=.012/max(np.max(abs(a)),1e-9)
  a*=g;gain_report[role]={'linear_gain':g,'reference_role':matches.get(role,[None])[0],'peak_dbfs':20*np.log10(max(np.max(abs(a)),1e-10))}
  save(OUT/'stems'/f'{role}.wav',a);music+=a;stems[role]=str(OUT/'stems'/f'{role}.wav')
  print('Rendered',role,flush=True)
 save(OUT/'music-only.wav',music)
 mix=music.copy()
 for role in ['dialogue','effects','ambience']:
  shutil.copy2(D4/'stems'/f'{role}.wav',OUT/'stems'/f'{role}.wav');mix+=read(OUT/'stems'/f'{role}.wav')
 mix[164*SR:166*SR]=0;save(OUT/'premaster.wav',mix)
 before=loudness(OUT/'premaster.wav');gain_db=-18-float(before['input_i'])
 ff(['-v','error','-i',OUT/'premaster.wav','-af',f'volume={gain_db}dB,aresample=192000,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true,aresample=48000','-c:a','pcm_f32le',OUT/'master-limited.wav'])
 master=read(OUT/'master-limited.wav')[:N];assert len(master)==N;master[164*SR:166*SR]=0;save(OUT/'mix.wav',master)
 after=loudness(OUT/'mix.wav')
 put(OUT/'mix.json',{'version':'D5 all-ukulele alternate','duration_seconds':180,'sample_rate':SR,'channels':2,'samples_per_channel':N,'master_gain_db':gain_db,'premaster_loudness':before,'master_loudness':after,'music_roles':list(ROLES),'render_gains':gain_report,'source':'Only the saved CC0 ukulele pitched/body/muted samples produce the new score; Roy is the accepted D4 stem. No oscillator, drum sample, piano, brass or string sample is used. Practical sound effects remain separate.','source_library':'Flight Fireball tenor / Mateusz Dabrowski / FreePats, CC0','source_url':'https://freepats.zenvoid.org/GuitarFamily/ukulele.html','paid_generations':0,'dialogue_effects_ambience':'Byte-identical D4 stems before common mastering gain','picture':'Original D4 encoded video stream retained without re-encoding, including its D4 picture-pass label','roy':'Byte-identical to D4 ukulele stem, including microtiming and playback perspective'})
 for start,duration,name in [(0,40,'opening-and-rehearsal'),(104,30,'pinterest-reveal'),(148,32,'ending')]:
  ff(['-v','error','-ss',start,'-i',OUT/'mix.wav','-t',duration,'-c:a','libmp3lame','-b:a','192k',OUT/'audio-review'/f'{name}.mp3'])
 ff(['-v','error','-i',OUT/'music-only.wav','-af',f'volume={gain_db}dB,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true','-c:a','libmp3lame','-b:a','192k',OUT/'audio-review/music-only.mp3'])
 print('Mastered',after,flush=True)
def export():
 ff(['-v','error','-i',D4/'first-trailer-finishing-d4.mp4','-i',OUT/'mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',48000,'-t',180,'-metadata','title=YOU CAN SEE EVERYTHING - D5 ukulele score alternate (D4 picture)','-movflags','+faststart',OUT/'first-trailer-ukulele-d5.mp4'])
 print('D5 exported; original encoded picture retained',flush=True)
if __name__=='__main__':
 for name in sys.argv[1:] or ['compose','score','audio','export']:globals()[name]()
