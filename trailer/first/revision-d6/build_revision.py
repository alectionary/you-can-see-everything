"""D6 user-notes pass: audible strums, original Dan exchange, physical documents, expanding cards."""
from pathlib import Path
import csv,hashlib,importlib.util,json,math,re,shutil,struct,subprocess,sys
import numpy as np,soundfile as sf
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');HERE=ROOT/'trailer/first/revision-d6';OUT=ROOT/'build/first-trailer-revision-d6';D4=ROOT/'build/first-trailer-finishing-d4';D5=ROOT/'build/first-trailer-ukulele-d5'
SR=48000;DURATION=191;N=DURATION*SR;FPS=24;W=1280;H=720
FONT=Path.home()/'Library/Fonts/LiberationSans-Bold.ttf';REGULAR=FONT.parent/'LiberationSans-Regular.ttf'
spec=importlib.util.spec_from_file_location('uke5',ROOT/'trailer/first/ukulele-d5/build_ukulele.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
INSERTS=[(79,2,'C01','YOU CAN SEE PARKING'),(104,2,'C02','YOU CAN SEE BETRAYAL'),(164,3,'C03','YOU CAN SEE BEYOND TRUTH'),(180,4,'C04','LEARN MORE ON PINTEREST: @YOUCANSEEEVERYTHINGFILMS')]
def shift(t):return float(t)+sum(d for at,d,_,_ in INSERTS if t>=at)
def shift_end(t):return float(t)+sum(d for at,d,_,_ in INSERTS if t>at)
def put(p,v):p.write_text(json.dumps(v,indent=2,default=lambda x:x.item())+'\n')
def init():
 for x in [HERE,HERE/'images',OUT,OUT/'speech',OUT/'lip-inputs',OUT/'mouths',OUT/'segments',OUT/'plates',OUT/'score',OUT/'stems',OUT/'contacts',OUT/'audio-review',OUT/'pdf-review']:x.mkdir(parents=True,exist_ok=True)
def ff(args,**kw):return subprocess.run(['ffmpeg','-y','-hide_banner','-v','error',*map(str,args)],check=True,**kw)
def rawmono(p,sr=SR):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar',str(sr),'-f','f32le','-']),'<f4').copy()
def read(p):
 a,sr=sf.read(p,dtype='float32',always_2d=True);assert sr==SR;return a
def save(p,a):sf.write(p,a,SR,subtype='PCM_24')
def add(a,z,t):
 i=round(t*SR);n=min(len(z),len(a)-i)
 if n>0:a[i:i+n]+=z[:n]
def remap(a):
 out=np.zeros((N,*a.shape[1:]),np.float32);previous=0;cursor=0
 for at,d,_,_ in INSERTS:
  stop=round(at*SR);count=stop-previous;out[cursor:cursor+count]=a[previous:stop];cursor+=count+round(d*SR);previous=stop
 return out
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
def prepare():
 init();old=list(csv.DictReader((D4/'timeline.csv').open()));timeline=[];cursor=0
 for row in old:
  r=dict(row);r.update(start_seconds=cursor,end_seconds=cursor+float(row['duration_seconds']),source_segment=row['segment']);timeline.append(r);cursor=r['end_seconds']
  for at,d,name,text in INSERTS:
   if float(row['end_seconds'])==at:
    timeline.append({'segment':name,'start_seconds':cursor,'end_seconds':cursor+d,'duration_seconds':d,'asset_ids':'new card','picture':text,'source_segment':''});cursor+=d
 assert cursor==DURATION and len(timeline)==44
 with (OUT/'timeline.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(timeline[0]));w.writeheader();w.writerows(timeline)
 oldtiming=json.loads((D4/'speech/timing.json').read_text());lines=list(csv.DictReader((D4/'dialogue.csv').open()));new=[];newlines=[]
 for item in oldtiming:
  if item['id']=='L04':continue
  r=dict(item)
  for k in ['start','actual_end','target_end','caption_end']:r[k]=shift(item[k])
  new.append(r);shutil.copy2(D4/'speech'/f"{item['id']}.wav",OUT/'speech'/f"{item['id']}.wav")
  line=dict(next(x for x in lines if x['line_id']==item['id']));line['start_seconds']=shift(float(line['start_seconds']));line['end_seconds']=shift(float(line['end_seconds']));newlines.append(line)
 # Restore both existing Dan recordings, using their natural durations and recovered original voice.
 question=rawmono(ROOT/'dialogue/v2/d04.mp3');active=np.flatnonzero(abs(question)>max(abs(question))*.012);question=question[max(0,active[0]-240):min(len(question),active[-1]+481)]
 question*=.34/max(abs(question));question[:240]*=np.linspace(0,1,240);question[-240:]*=np.linspace(1,0,240)
 answer=rawmono(D4/'speech/L04.wav');save(OUT/'speech/L04a.wav',question);shutil.copy2(D4/'speech/L04.wav',OUT/'speech/L04b.wav')
 for lid,t,z,text,path,cap in [('L04a',18.4,question,'Why would I deceive you?','dialogue/v2/d04.mp3',19.75),('L04b',20.25,answer,'There’s no reason for me to do that.','dialogue/v2/d05.mp3',21.95)]:
  assert t+len(z)/SR<cap
  new.append({'id':lid,'speaker':'DAN','start':t,'actual_end':t+len(z)/SR,'target_end':cap,'caption_end':cap,'source':path,'provider':'original teaser','reused':True})
  newlines.append({'line_id':lid,'start_seconds':t,'end_seconds':cap,'speaker':'DAN','text':text,'source':'reuse '+path+'; original established Dan / Eric recording','segment':'T04'})
 new.sort(key=lambda r:r['start']);newlines.sort(key=lambda r:float(r['start_seconds']));assert len(new)==32
 put(OUT/'speech/timing.json',new)
 with (OUT/'dialogue.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(lines[0]));w.writeheader();w.writerows(newlines)
 captions='\n\n'.join(f"{i}\n{stamp(line['start'])} --> {stamp(line['caption_end'])}\n{next(x['text'] for x in newlines if x['line_id']==line['id'])}" for i,line in enumerate(new,1))+'\n';(OUT/'captions.srt').write_text(captions)
 # Role-specific lip drivers retain local positions; later scene shifts do not change mouth timing within a shot.
 for segment,start,dur in [('T04',18,4),('T08',34,3),('T10',40,8),('T22',98,6),('T26',122,4),('T30',142,3)]:
  audio=np.zeros(round(dur*SR),np.float32)
  for item in new:
   if item['speaker']=='DAN' and shift(start)<=item['start']<shift(start)+dur:
    add(audio,rawmono(OUT/'speech'/f"{item['id']}.wav"),item['start']-shift(start))
  sf.write(OUT/'lip-inputs'/f'{segment}.wav',audio,SR,subtype='PCM_16')
 put(OUT/'edit-plan.json',{'duration_seconds':DURATION,'old_duration_seconds':180,'added_seconds':11,'minimum_segment_seconds':2,'cards':INSERTS,'title_attack':173,'silence':[171,173],'music_ends':177,'cta':[187,191],'dan_opening':'Original d04 and d05, both on Dan; no new TTS','rules_audit':'All original holds retained; four standalone cards added; no shot shortened. Dialogue shifts only with insertions, plus explicitly requested restored opening exchange.'})
 print('Prepared 44 segments / 191 seconds / 32 spoken cues',flush=True)

def compose():
 init();d=json.loads((D5/'score/events.json').read_text());events={}
 for role,es in d['events'].items():
  events[role]=[]
  for e in es:
   r=dict(e);r['t']=shift(e['t']);end=shift_end(e['t']+e['d'])
   # Sustained resonance continues underneath inserted cards; transient note lengths stay intact.
   if role=='bloom' and e['t']+e['d'] in [79,104,164]:end=shift(e['t']+e['d'])
   r['d']=end-r['t'];events[role].append(r)
 # Roy's opening is now explicitly strummed; his continuous middle performance is preserved.
 chords={57:[57,60,64,69],64:[55,59,64,67],60:[55,60,64,67],61:[57,61,64,69]}
 for e in events['roy']:
  if e['t']<18:e['notes']=chords[e['notes'][0]];e['articulation']='down-strum, 13ms between strings';e['d']=min(1.0,e['d']);e['v']=72 if e['t']<8 else 64
 def add_event(role,t,d,notes,v):events[role].append({'t':t,'d':d,'notes':notes,'v':v,'source_staff':'new card extension'})
 for t,n in [(79,33),(80,34),(106,33),(107,34)]:add_event('low',t,.75,[n],70)
 for t,n in [(79.5,57),(80.5,58),(106.5,64),(107.5,60)]:add_event('plucks',t,.5,[n],63)
 for t in [106,107]:add_event('body',t,.25,[48],50)
 for j,t in enumerate(np.arange(168,171,.5)):
  add_event('low',float(t),.25,[33 if j%2==0 else 34],104+j)
  add_event('body',float(t),.25,[47 if j%3==0 else 48],86+j)
 for j,t in enumerate([168,169,170]):add_event('plucks',t,.5,[58+j,59+j,66],94+j*4)
 add_event('grit',168,3,[33,39,46],108)
 for es in events.values():es.sort(key=lambda e:e['t'])
 d.update(version='D6 user-notes revision',duration_seconds=DURATION,events=events,title='One shared attack at 173; decay ends by 177',gates=[[171,173],[177,191]],opening='Clearly ringing four-string chords with staggered attacks; original wrong chord retained, muted at 3.48; clean restart under the interview question.')
 put(OUT/'score/events.json',d)
 with (OUT/'score/event-cues.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['role','onset_seconds','release_seconds','midi_notes','velocity'])
  for role,es in events.items():
   for e in es:w.writerow([role,e['t'],e['t']+e['d'],' '.join(map(str,e['notes'])),e['v']])
 print('Extended written score, bass, textures and rhythm through new cards',flush=True)

def fix_midi_meter(path):
 data=path.read_bytes();length=struct.unpack('>I',data[18:22])[0]
 import struct as st
 def variable(n):
  out=[n&127];n>>=7
  while n:out.insert(0,(n&127)|128);n>>=7
  return bytes(out)
 conductor=bytes.fromhex('00ff51030f424000ff580404021808')+variable(188*480)+bytes.fromhex('ff580403021808')+variable(3*480)+bytes.fromhex('ff2f00')
 path.write_bytes(data[:14]+b'MTrk'+st.pack('>I',len(conductor))+conductor+data[22+length:])
def mouths():
 subprocess.run([sys.executable,str(HERE/'correct_mouths.py')],check=True)
def score():
 init();d=json.loads((OUT/'score/events.json').read_text());events=d['events']
 # Reuse the open-source notation/MIDI routines with an explicit 191-second endpoint and partial final bar.
 code=(ROOT/'trailer/first/ukulele-d5/build_ukulele.py').read_text();code=code.replace('180*480','191*480').replace('range(45)','range(48)').replace('a=bar*4;b=a+4','a=bar*4;b=min(a+4,191)')
 ns=dict(b.__dict__);exec(compile(code,str(HERE/'notation-adapter.py'),'exec'),ns);ns['OUT']=OUT
 ns['midi'](events)
 fix_midi_meter(OUT/'score/ukulele-score-d5.mid')
 glob='\\numericTimeSignature \\time 4/4 \\tempo 4 = 60 \\key a \\minor\n'
 cues={0:'Roy / clear strums',18:'Dan exchange',40:'Casting',62:'Corporate review',79:'PARKING',84:'Publicity',106:'BETRAYAL',108:'Roy introduction',114:'Roy plays',130:'Authenticity',152:'Fracture',168:'BEYOND TRUTH',171:'Silence',173:'Single title attack',177:'Roy / room only',187:'Pinterest CTA'}
 for t in range(DURATION):
  if t==188:glob+='\\time 3/4 '
  if t in cues:glob+=f'\\mark \\markup \\tiny "{t//60}:{t%60:02d} {cues[t]}" '
  glob+='s4 '
  if (t+1)%4==0 or t==190:glob+='|\n'
  if t+1 in [32,64,96,128,160]:glob+='\\pageBreak '
  elif (t+1)%16==0 and t+1<176:glob+='\\break '
 s='''\\version "2.24.3"
#(set-global-staff-size 15)
\\header { title = "YOU CAN SEE EVERYTHING" subtitle = "D6 - ukulele score / editorial revision" subsubtitle = "3:11 | quarter = 60 | sounding studio pitches" composer = "Original trailer arrangement" tagline = ##f }
\\paper { #(set-paper-size "a3") indent = 39\\mm short-indent = 14\\mm top-margin = 12\\mm bottom-margin = 12\\mm system-system-spacing.basic-distance = #25 }
'''
 s+='global = { '+glob+' }\n'
 for role,es in events.items():s+=role+'Music = \\absolute { '+ns['notation'](es,role=='body')+' }\n'
 s+='\\markup \\column { \\small "Four seconds per full bar; final bar is 3/4. Stagger opening strums by 13ms per string." \\small "Roy retains natural microtiming. Low notes, sustains and distortion are studio transformations." \\small "Round body note = tap; cross = muted strum. MIDI supplies notes/timing; WAVs supply the finished timbres." \\small "Cards add eleven seconds. Silence 2:51-2:53; title attack 2:53; no music after 2:57." }\n'
 s+='\\score { <<\n'
 for role,(name,short,clef,_) in b.ROLES.items():
  extra=' \\override StaffSymbol.line-count = #1' if role=='body' else ''
  s+=f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}"{extra} }} << \\global {{ \\clef {clef} \\{role}Music }} >>\n'
 s+='>> \\layout { \\context { \\Score \\override RehearsalMark.self-alignment-X = #LEFT } } }\n'
 p=OUT/'score/ukulele-score-d6.ly';p.write_text(s);r=subprocess.run(['lilypond','-dno-point-and-click','-o',str(p.with_suffix('')),str(p)],text=True,capture_output=True);(OUT/'score/compile.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
 # The adapter emits D5 interchange basename; label the completed new score accurately.
 shutil.move(OUT/'score/ukulele-score-d5.mid',OUT/'score/ukulele-score-d6.mid')
 print('D6 score and MIDI compiled',flush=True)

def audio():
 init();events=json.loads((OUT/'score/events.json').read_text())['events'];timing=json.loads((OUT/'speech/timing.json').read_text());duck=np.ones(N,np.float32)
 for line in timing:duck[max(0,round((line['start']-.07)*SR)):min(N,round((line['actual_end']+.13)*SR))]=.28
 idx=np.arange(0,N,240);coarse=duck[idx]
 for _ in range(4):coarse=np.convolve(coarse,[.2,.6,.2],mode='same')
 duck=np.interp(np.arange(N),idx,coarse).astype(np.float32);music=np.zeros((N,2),np.float32)
 oldroy=read(D5/'stems/roy.wav');roy=remap(oldroy);roy[:18*SR]=0
 for e in events['roy']:
  if e['t']>=18:continue
  length=min(2.5,3.48-e['t']) if e['t']<8 else min(2.1,18-e['t']);z=np.zeros(round(length*SR),np.float32)
  for j,n in enumerate(e['notes']):
   a=b.sample(n);a=b.envelope(a,.006,.08);a=a*np.exp(-np.arange(len(a))/SR/1.3)
   start=round(j*.013*SR);count=min(len(a),len(z)-start)
   if count>0:z[start:start+count]+=a[:count]/max(abs(a))
  z=b.envelope(z,.008,.06);z*= (.23 if e['t']<8 else .155)/max(abs(z));add(roy,b.stereo(z),e['t'])
 roy[:18*SR]*=(.48+.52*duck[:18*SR,None]);save(OUT/'stems/roy.wav',roy);music+=roy
 gains=json.loads((D5/'mix.json').read_text())['render_gains'];pans={'plucks':-.12,'low':0,'bloom':.12,'grit':-.08,'body':.14,'reverse':-.18}
 report={}
 for role,es in events.items():
  if role=='roy':continue
  bus=np.zeros(N,np.float32)
  for e in es:
   render=dict(e)
   if e['t']==173:render['t']=166
   a=b.render_voice(role,render);add(bus,a,e['t'])
  bus*=duck
  if role in ['plucks','bloom','body','grit']:
   t=np.arange(N,dtype=np.float32)/SR;m=(t>=114)&(t<122);bus[m]*=.15+.85*(t[m]-114)/8
  a=b.stereo(bus,pans[role])*gains[role]['linear_gain'];a[171*SR:173*SR]=0;a[177*SR:]=0
  a[round(170.95*SR):171*SR]*=np.linspace(1,0,round(.05*SR))[:,None];a[round(176.9*SR):177*SR]*=np.linspace(1,0,round(.1*SR))[:,None]
  save(OUT/'stems'/f'{role}.wav',a);music+=a;report[role]={'linear_gain':gains[role]['linear_gain'],'source':'Ukulele recordings, same transformation as D5; extended event map'};print('Rendered',role,flush=True)
 save(OUT/'music-only.wav',music)
 dialogue=remap(read(D4/'stems/dialogue.wav'));dialogue[18*SR:22*SR]=0
 for lid in ['L04a','L04b']:
  line=next(x for x in timing if x['id']==lid);add(dialogue,b.stereo(rawmono(OUT/'speech'/f'{lid}.wav')),line['start'])
 save(OUT/'stems/dialogue.wav',dialogue);mix=music+dialogue
 for role in ['effects','ambience']:
  a=remap(read(D4/'stems'/f'{role}.wav'));save(OUT/'stems'/f'{role}.wav',a);mix+=a
 mix[171*SR:173*SR]=0;save(OUT/'premaster.wav',mix)
 before=b.loudness(OUT/'premaster.wav');gain=-18-float(before['input_i'])
 ff(['-i',OUT/'premaster.wav','-af',f'volume={gain}dB,aresample=192000,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true,aresample=48000','-c:a','pcm_f32le',OUT/'master-limited.wav'])
 master=read(OUT/'master-limited.wav')[:N];master[171*SR:173*SR]=0;save(OUT/'mix.wav',master);after=b.loudness(OUT/'mix.wav')
 put(OUT/'mix.json',{'duration_seconds':DURATION,'sample_rate':SR,'channels':2,'master_gain_db':gain,'premaster_loudness':before,'master_loudness':after,'roles':report,'opening':'Clearly ringing four-string staggered strums; original wrong chord and restart retained; no body-percussion score in first 18 seconds. Roy foreground peak raised.','speech':'Original Dan d04 restored and d05 moved later within T04; all other accepted PCM speech preserved, shifted with inserted cards.','silence':[171,173],'title_attack':173,'music_ends':177,'new_runway_generations':0,'new_elevenlabs_generations':0})
 for start,duration,name in [(0,26,'opening-restored-dan'),(75,13,'parking-card'),(100,35,'betrayal-and-pinterest'),(152,39,'ending-and-cards')]:ff(['-ss',start,'-i',OUT/'mix.wav','-t',duration,'-c:a','libmp3lame','-b:a','192k',OUT/'audio-review'/f'{name}.mp3'])
 print('D6 mix mastered',after,flush=True)

def center(im,y,text,size,bold=True):
 f=ImageFont.truetype(str(FONT if bold else REGULAR),size);d=ImageDraw.Draw(im);box=d.textbbox((0,0),text,font=f)
 while box[2]-box[0]>W-110:size-=1;f=ImageFont.truetype(str(FONT if bold else REGULAR),size);box=d.textbbox((0,0),text,font=f)
 d.text(((W-(box[2]-box[0]))/2,y),text,font=f,fill=(242,239,229))
def card(name):
 im=Image.new('RGB',(W,H),'black')
 if name in ['C01','C02','C03','T38']:
  word={'C01':'PARKING','C02':'BETRAYAL','C03':'BEYOND TRUTH','T38':'EVERYTHING'}[name];size={'C01':68,'C02':82,'C03':94,'T38':112}[name];center(im,260,'YOU CAN SEE',42 if name=='C01' else 49 if name=='C02' else 56);center(im,327,word,size)
 else:center(im,282,'LEARN MORE ON PINTEREST',32);center(im,350,'@YOUCANSEEEVERYTHINGFILMS',43)
 return im
def tagged_motion(source,target,duration):
 vf=f"drawbox=x=12:y=12:w=194:h=28:color=0x0a0e12:t=fill,drawtext=fontfile={FONT}:text='REVISION D6':fontsize=16:fontcolor=white:x=22:y=18"
 ff(['-i',source,'-t',duration,'-vf',vf,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',target])
def picture():
 init();rows=list(csv.DictReader((OUT/'timeline.csv').open()));sources=[]
 for row in rows:
  name=row['segment'];target=OUT/'segments'/f'{name}.mp4';dur=row['duration_seconds'];source=D4/'segments'/f'{name}.mp4';kind='preserved D4 segment'
  if name in ['C01','C02','C03','C04','T38']:
   source=OUT/'plates'/f'{name}.png';card(name).save(source);kind='new intertitle'
   if not target.exists():ff(['-loop','1','-framerate',24,'-i',source,'-t',dur,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',target])
  elif name in ['T14','T29','T33']:
   source=HERE/'images'/f'{name}.png';assert source.exists(),source;kind='generated physical document photograph'
   if not target.exists():ff(['-loop','1','-framerate',24,'-i',source,'-t',dur,'-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720','-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',target])
  elif name in ['T04','T08','T10','T22','T26','T30']:
   source=OUT/'mouths'/f'{name}.mp4';assert source.exists(),source;kind='Dan speech-window mouth correction'
   if not target.exists():tagged_motion(source,target,dur)
  elif not target.exists():
   if name=='T37':shutil.copy2(source,target)
   else:tagged_motion(source,target,dur)
  sources.append({'segment':name,'source':str(source),'kind':kind,'duration':float(dur)})
 put(OUT/'picture-sources.json',sources);(OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in rows));ff(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4']);print('44 picture segments assembled',flush=True)
def export():
 style='FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48'
 ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',f"subtitles={OUT/'captions.srt'}:fontsdir={FONT.parent}:force_style='{style}'",'-map','0:v','-map','1:a','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar',SR,'-t',DURATION,'-metadata','title=YOU CAN SEE EVERYTHING - D6 editorial revision','-movflags','+faststart',OUT/'first-trailer-revision-d6.mp4']);print('D6 exported',flush=True)
if __name__=='__main__':
 for name in sys.argv[1:] or ['prepare','compose','score','audio','mouths','picture','export']:globals()[name]()
