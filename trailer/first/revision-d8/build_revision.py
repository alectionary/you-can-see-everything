"""D8 user-directed editorial rebuild. All assets/local outputs saved; no paid API calls."""
from pathlib import Path
import csv,json,hashlib,math,shutil,subprocess,sys,importlib.util,textwrap,struct
from functools import lru_cache
import cv2,numpy as np,soundfile as sf
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');HERE=ROOT/'trailer/first/revision-d8';OUT=ROOT/'build/first-trailer-revision-d8';D7=ROOT/'build/first-trailer-revision-d7';D3=ROOT/'build/first-trailer-picture-pass-d3';RAW=ROOT/'clips/first/picture-pass-d3';SR=48000;FPS=24;W=1280;H=720;DUR=197;N=DUR*SR
spec=importlib.util.spec_from_file_location('b7',ROOT/'trailer/first/revision-d7/build_revision.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
FONT=b.FONT;REG=b.REG
def ff(args):return b.ff(args)
def put(p,x):b.put(p,x)
def rows():return list(csv.DictReader((OUT/'timeline.csv').open()))
def start(n):return float(next(x for x in rows() if x['segment']==n)['start_seconds'])
def init():
 for s in ['speech','stems','plates','score','contacts','segments','audio-review','pdf-review']:(OUT/s).mkdir(parents=True,exist_ok=True)
def stamp(t):return b.b.stamp(t)
def prepare():
 init();old=list(csv.DictReader((D7/'timeline.csv').open()));order=[x['segment'] for x in old];order.remove('C01');order.insert(order.index('T17'),'C01');by={x['segment']:x for x in old};new=[];cursor=0
 pictures={'T03':'YOU CAN SEE THE TRUTH, 12 seconds until Dan; no visible hands','T04':'Simultaneous Dan and original Fielder reaction, squint on that','T05':'Continue the original simultaneous take; Again before next take','T06':'Take 2: identical Dan assurance playback, new Fielder reaction','T07':'Take 3: identical Dan assurance playback, new Fielder reaction, then question; extended 4 seconds','T08':'Pinterest DM: Dan to Nathan, I thought you looked confused','T09':'Same iPhone DM: Nathan replies I was','T10':'YOU CAN SEE A CHARACTER HE CREATED; existing refusal/lookalike exchange','T11':'Candidate A moving video pulls back into glary MacBook editing board','T12':'Candidate B moving video in the MacBook editing board','T13':'Candidate C moving video in the MacBook editing board','T15':'YOU CAN SEE CORPORATE COMMUNICATIONS','C01':'YOU CAN SEE PARKING before actual lot','T18':'Friendly architectural parking plan and demolition permit','T21':'YOU CAN SEE TROLLING with accepted Fielder voice','T22':'Dan Pinterest post embeds painting destruction; absurd angry reaction count','T23':'Roy instrument introduction: hands rest; no strum audio','T24':'Same continuous native Roy performance; audio attacks follow actual strokes','T25':'Pinterest DM, Nathan asks Did you arrange this','T26':'Same DM, Dan says Roy chose the song, then blocks Nathan','T28':'Editor/Nathan scene pulls back into Nathan post: I didn’t know','T35':'Dan signature line visibly remains Dan','T36':'Roy/lawyer DM screenshot pulls out to a Times Square billboard; extended 2 seconds','C04':'LEARN MORE ON PINTEREST / @YOU_CAN_SEE_EVERYTHING'}
 for n in order:
  r=dict(by[n]);dur=float(r['duration_seconds'])+(4 if n=='T07' else 2 if n=='T36' else 0);r.update(start_seconds=cursor,end_seconds=cursor+dur,duration_seconds=dur,picture=pictures.get(n,r['picture']));new.append(r);cursor+=dur
 assert cursor==DUR
 with (OUT/'timeline.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(new[0]));w.writeheader();w.writerows(new)
 newby={x['segment']:x for x in new};mapping={n:float(newby[n]['start_seconds'])-float(by[n]['start_seconds']) for n in order}
 timing=json.loads((D7/'speech/timing.json').read_text());lines=list(csv.DictReader((D7/'dialogue.csv').open()));lineby={x['line_id']:x for x in lines}
 for e in timing:
  lid=e['id'];segment=lineby[lid]['segment'];delta=mapping[segment]+(4 if lid=='L06' else 0)
  for k in ['start','actual_end','target_end','caption_end']:e[k]+=delta
  lineby[lid]['start_seconds']=e['start'];lineby[lid]['end_seconds']=e['caption_end'];shutil.copy2(D7/'speech'/f'{lid}.wav',OUT/'speech'/f'{lid}.wav')
 for k,t in [('L04r2',26.25),('L04r3',30.25)]:
  z=next(x for x in timing if x['id']=='L04b');dur=z['actual_end']-z['start'];r=dict(z,id=k,start=t,actual_end=t+dur,target_end=t+1.7,caption_end=t+1.7);timing.append(r);shutil.copy2(OUT/'speech/L04b.wav',OUT/'speech'/f'{k}.wav');line=dict(lineby['L04b'],line_id=k,start_seconds=t,end_seconds=t+1.7,segment='T06' if k.endswith('2') else 'T07',source='EXACT L04b audio repeated, no regeneration or retiming');lines.append(line)
 timing.sort(key=lambda e:e['start']);lines.sort(key=lambda e:float(e['start_seconds']));put(OUT/'speech/timing.json',timing)
 with (OUT/'dialogue.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(lines[0]));w.writeheader();w.writerows(lines)
 (OUT/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(e['start'])} --> {stamp(e['caption_end'])}\n{next(x['text'] for x in lines if x['line_id']==e['id'])}" for i,e in enumerate(timing,1))+'\n')
 # Hand-motion measurements are source-based; annotate reviewed gesture exclusions and final edit positions.
 motion=json.loads((OUT/'hand-motion.json').read_text())
 for m in motion:
  m['timeline_start']={'opening':0,'apology':8,'middle':start('T23'),'ending':start('T39')}[m['key']]
  if m['key']=='ending':m['onsets_local']=[t for t in m['onsets_local'] if t>0]
  if m['key']=='middle':m['onsets_local']=[t for t in m['onsets_local'] if t>=6];m['visual_review']='First six seconds are introduction and a hand opening/damping gesture, not playing. No strum is sounded there.'
  m['onsets_global']=[round(t+m['timeline_start'],6) for t in m['onsets_local']]
 put(OUT/'hand-motion.json',motion)
 put(OUT/'edit-plan.json',{'duration':DUR,'prior_duration':191,'added_seconds':6,'minimum_hold':2,'extensions':{'T07':4,'T36':2},'no_shot_shortened':True,'cards_explicitly_over_spoken_audio':True,'parking_card_precedes_lot':True,'handle':'@YOU_CAN_SEE_EVERYTHING','original_Dan_replays':[20.25,26.25,30.25],'that_relative_to_assurance_start':1.05,'Fielder_source_squint_anchors':[4.4,3.9,2.7],'motion':'Locked static cards/screens; mathematically smooth subpixel pullbacks only; no zoompan shake','RULES.md_audit':'All original holds retained, third rehearsal extended four seconds and billboard two seconds. Full trailer changes and text-over-voice cards explicitly requested by user. Dialogue words and accepted recordings preserved; two exact Dan audio replays added. Final encoded delivery will be audited.'})
 print('D8 prepared: 197 seconds, 44 holds, 34 voice cues',flush=True)
def remap(a):
 old={x['segment']:x for x in csv.DictReader((D7/'timeline.csv').open())};out=np.zeros((N,*a.shape[1:]),np.float32)
 for r in rows():
  p=old[r['segment']];i=round(float(p['start_seconds'])*SR);count=round(float(p['duration_seconds'])*SR);j=round(float(r['start_seconds'])*SR);out[j:j+count]=a[i:i+count]
  if r['segment']=='T07':out[j+count:j+2*count]=a[i:i+count]
  if r['segment']=='T36':
   out[j+count:j+count+2*SR]=a[i+count-2*SR:i+count]
   fade=round(.02*SR);out[j+count-fade:j+count]*=np.linspace(1,0,fade).reshape((-1,)+(1,)*(out.ndim-1));out[j+count:j+count+fade]*=np.linspace(0,1,fade).reshape((-1,)+(1,)*(out.ndim-1))
 return out
def compose():
 d=json.loads((D7/'score/events.json').read_text());old=list(csv.DictReader((D7/'timeline.csv').open()));new={x['segment']:x for x in rows()};events={}
 for role,es in d['events'].items():
  events[role]=[]
  if role=='roy':continue
  for e in es:
   r=next(x for x in old if float(x['start_seconds'])<=e['t']<float(x['end_seconds']));n=new[r['segment']];z=dict(e,t=e['t']+float(n['start_seconds'])-float(r['start_seconds']));events[role].append(z)
   if r['segment']=='T07':events[role].append(dict(z,t=z['t']+4))
   if r['segment']=='T36' and e['t']+e['d']>166:
    lo=max(e['t'],166);hi=min(e['t']+e['d'],168)
    if hi>lo:events[role].append(dict(e,t=172+lo-166,d=hi-lo,source_staff='D8 billboard extension'))
 chords=[[57,60,64,69],[55,59,64,67],[55,60,64,67],[55,59,64,67]]
 for m in json.loads((OUT/'hand-motion.json').read_text()):
  for i,t in enumerate(m['onsets_global']):
   local=t-m['timeline_start'];notes=chords[(int(local)//1)%4]
   if m['key']=='opening' and local>=7:notes=[57,61,64,69]
   events['roy'].append({'t':t,'d':min(.5,m['timeline_start']+m['duration']-t),'notes':notes,'v':54 if m['key']=='apology' else 74 if i%2==0 else 65,'articulation':'palm-muted' if m['key']=='apology' else 'ringing','source_staff':'verified hand-motion frame '+str(round(local*24)),'motion_key':m['key']})
 for role in ['plucks','body']:events[role]=[e for e in events[role] if not 112<=e['t']<118]
 for es in events.values():es.sort(key=lambda e:e['t'])
 d.update(version='D8 hand-synchronized editorial score',duration_seconds=DUR,events=events,gates=[[177,179],[193,197]],title='One title attack at 179; transformed score ends 183; Roy plays to 193',opening='Roy stops at 12. No Roy strum events at 12-18 or during the six-second song introduction. Onsets follow the actual source hand-motion peaks, not a regular musical grid.')
 put(OUT/'score/events.json',d)
def audio():
 init();events=json.loads((OUT/'score/events.json').read_text())['events'];timing=json.loads((OUT/'speech/timing.json').read_text());dialogue=np.zeros((N,2),np.float32)
 for e in timing:b.b.add(dialogue,b.b.b.stereo(b.b.rawmono(OUT/'speech'/f"{e['id']}.wav")),e['start'])
 b.b.save(OUT/'stems/dialogue.wav',dialogue);music=np.zeros((N,2),np.float32);roy=music.copy()
 for e in events['roy']:
  z=b.strum(dict(e,articulation='palm-muted' if e['motion_key']=='apology' else 'ringing'));t=e['t'];end=12 if t<12 else 126 if t<150 else 193;z=z[:max(0,round((end-t)*SR))];z=z.copy();release=min(round(.045*SR),len(z));z[-release:]*=np.linspace(1,0,release)[:,None]
  # Keep voices clear without suppressing the visible string attack.
  gain=.68 if any(x['start']-.04<=t<x['actual_end']+.1 for x in timing) else .95;b.b.add(roy,z*gain,t)
 b.b.save(OUT/'stems/roy.wav',roy);music+=roy
 for role in ['plucks','low','bloom','grit','body','reverse']:
  a=remap(b.b.read(D7/'stems'/f'{role}.wav'))
  if role in ['plucks','body']:
   gate=np.interp(np.arange(N)/SR,[0,111.95,112,118,118.05,125.95,126,DUR],[1,1,0,0,.12,.12,1,1]).astype(np.float32);a*=gate[:,None]
  b.b.save(OUT/'stems'/f'{role}.wav',a);music+=a
 b.b.save(OUT/'music-only.wav',music);mix=music+dialogue
 for role in ['effects','ambience']:
  a=remap(b.b.read(D7/'stems'/f'{role}.wav'));b.b.save(OUT/'stems'/f'{role}.wav',a);mix+=a
 mix[177*SR:179*SR]=0;mix[193*SR:]=0;b.b.save(OUT/'premaster.wav',mix);before=b.b.b.loudness(OUT/'premaster.wav');gain=-18-float(before['input_i'])
 ff(['-i',OUT/'premaster.wav','-af',f'volume={gain}dB,aresample=192000,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true,aresample=48000','-c:a','pcm_f32le',OUT/'master-limited.wav']);master=b.b.read(OUT/'master-limited.wav')[:N];master[177*SR:179*SR]=0;master[193*SR:]=0;b.b.save(OUT/'mix.wav',master);loud=b.b.b.loudness(OUT/'mix.wav');put(OUT/'mix.json',{'master_gain_db':gain,'loudness':loud,'hand_sync':'Each clean instrument attack follows reviewed visible hand motion, with idle/damping introduction excluded','dialogue':'32 accepted files preserved, two exact byte-identical Dan repeats','score_extended_seconds':6,'black_silence':[177,179],'title_attack':179,'score_ends':183,'diegetic_ends':193})
 for ss,dur,key in [(0,44,'opening-rehearsal'),(108,24,'roy-synchronization'),(164,33,'billboard-and-ending')]:ff(['-ss',ss,'-i',OUT/'mix.wav','-t',dur,'-c:a','libmp3lame','-b:a','192k',OUT/'audio-review'/f'{key}.mp3'])
 print('D8 sound mastered',loud,flush=True)
@lru_cache(128)
def font(size,bold=False):return ImageFont.truetype(str(FONT if bold else REG),size)
def txt(im,xy,s,size=24,color='#212124',bold=False):ImageDraw.Draw(im).text(xy,s,font=font(size,bold),fill=color)
def center(im,y,s,size=50,color='#f1eee7'):
 d=ImageDraw.Draw(im)
 while d.textbbox((0,0),s,font=font(size,True))[2]>W-110:size-=1
 width=d.textlength(s,font=font(size,True));txt(im,((W-width)/2,y),s,size,color,True)
def card(n):
 im=Image.new('RGB',(W,H),'black');words={'T03':['THE TRUTH'],'T10':['A CHARACTER','HE CREATED'],'T15':['CORPORATE','COMMUNICATIONS'],'T21':['TROLLING'],'C04':['@YOU_CAN_SEE_EVERYTHING']}
 if n=='C04':center(im,285,'LEARN MORE ON PINTEREST',34);center(im,356,words[n][0],48)
 else:
  ls=words[n];center(im,218 if len(ls)==2 else 265,'YOU CAN SEE',43)
  for j,line in enumerate(ls):center(im,(294 if len(ls)==2 else 334)+j*84,line,75 if len(ls)==2 else 94)
 return im
def readframes(path,ss=0,dur=None):
 c=cv2.VideoCapture(str(path));c.set(cv2.CAP_PROP_POS_MSEC,ss*1000);out=[];count=round(dur*24) if dur else int(c.get(cv2.CAP_PROP_FRAME_COUNT))
 for i in range(count):
  ok,z=c.read()
  if not ok:break
  out.append(cv2.cvtColor(z,cv2.COLOR_BGR2RGB))
 c.release();assert out,path;return out
def get(frames,t):return frames[min(max(round(t*24),0),len(frames)-1)]
def encode(path,duration,fn):
 proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-video_size','1280x720','-framerate','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',str(path)],stdin=subprocess.PIPE)
 try:
  for i in range(round(duration*24)):
   im=fn(i/24);z=np.asarray(im,dtype=np.uint8);assert z.shape==(720,1280,3),z.shape;proc.stdin.write(z.tobytes())
 finally:proc.stdin.close()
 assert proc.wait()==0
def still(n,im,duration):
 p=OUT/'plates'/f'{n}.png';im.save(p);ff(['-loop','1','-framerate',24,'-i',p,'-t',duration,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',OUT/'segments'/f'{n}.mp4'])
def ease(t):t=np.clip(t,0,1);return t*t*(3-2*t)
def warp(im,dst):
 z=np.asarray(im);h,w=z.shape[:2];mat=cv2.getPerspectiveTransform(np.float32([[0,0],[w,0],[w,h],[0,h]]),np.float32(dst));return cv2.warpPerspective(z,mat,(W,H),flags=cv2.INTER_LINEAR)
def quad():return np.float32([[0,0],[W,0],[W,H],[0,H]])
def view(im,viewport):return warp(im,project(cv2.getPerspectiveTransform(np.float32(viewport),quad()),quad()))
def project(mat,points):return cv2.perspectiveTransform(np.float32(points).reshape(1,-1,2),mat)[0]
def composite_screen(base,screen,dst,glare=0):
 z=warp(screen,dst);mask=warp(np.ones((screen.shape[0],screen.shape[1],3),np.uint8)*255,dst).astype(np.float32)/255;out=np.asarray(base).astype(np.float32)*(1-mask)+z.astype(np.float32)*mask
 if glare:out=out*(1-glare*mask)+np.asarray(base).astype(float)*glare*mask
 return np.clip(out,0,255).astype(np.uint8)
def split_takes():
 dan=readframes(D7/'performance/dan-test-native.mp4');orig=readframes(next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4')));p2=readframes(ROOT/'clips/first/fielder-rehearsal-test-01.mov');p3=readframes(RAW/'fielder_practice.mp4');speak=readframes(D7/'performance/fielder-main-native.mp4',0,4)
 def compose(t,take):
  first=take==1;di=get(dan,min(t,3.65) if first else min(2+t,3.65));local=t if first else t
  if first:fi=get(orig,1.1+t);fc=(0,120,720,900)
  else:
   fi=get(p2,2.6+t) if take==2 else get(p3,1.4+min(t,3.9));fc=(320,10,960,700)
   if take==3 and t>=4:fi=get(speak,t-4)
  im=Image.new('RGB',(W,H),'#090b0c');left=Image.fromarray(di).crop((350,30,925,670)).resize((610,650),Image.Resampling.LANCZOS);right=Image.fromarray(fi).crop(fc).resize((610,650),Image.Resampling.LANCZOS);im.paste(left,(20,44));im.paste(right,(650,44));txt(im,(24,12),f'INTERVIEW / TAKE {take:02}',18,'#dedbd2',True);txt(im,(655,12),'NATHAN / REACTION',18,'#dedbd2',True);return im
 encode(OUT/'takes-01.mp4',8,lambda t:compose(t,1))
 for n,ss in [('T04',0),('T05',4)]:ff(['-ss',ss,'-i',OUT/'takes-01.mp4','-t',4,'-an','-c:v','libx264','-crf',18,'-preset','fast',OUT/'segments'/f'{n}.mp4'])
 encode(OUT/'segments/T06.mp4',4,lambda t:compose(t,2));encode(OUT/'segments/T07.mp4',8,lambda t:compose(t,3))
 put(OUT/'rehearsal-sync.json',{'Dan_source':'D7/performance/dan-test-native.mp4','first_assurance_source_start':2,'repeated_assurance_source_start':2,'Dan_audio_files':['L04b','L04r2','L04r3'],'first_squint_global':21.3,'take2_squint_global':27.3,'take3_squint_global':31.3,'squint_word':'that','only_reaction_performance_changes':True})
def bubble(im,xy,s,outgoing=False,size=28,width=400):
 d=ImageDraw.Draw(im);lines=textwrap.wrap(s,width=max(8,int(width/(size*.50))));he=len(lines)*(size+7)+30;x,y=xy;d.rounded_rectangle((x,y,x+width,y+he),radius=22,fill='#bd2031' if outgoing else '#ecebed')
 for j,line in enumerate(lines):txt(im,(x+16,y+13+j*(size+7)),line,size,'white' if outgoing else '#262628')
 return y+he
def phone_ui(kind,t):
 im=Image.new('RGB',(520,920),'#faf9f7');d=ImageDraw.Draw(im);txt(im,(32,24),'9:41',22,bold=True);txt(im,(340,24),'•••  ▰',20);txt(im,(28,80),'‹',42,'#bb2434');name='Dan' if kind=='confused' else 'Nathan';txt(im,(82,88),name,29,bold=True);txt(im,(82,124),'Pinterest · Messages',21,'#77767a');d.line((20,166,500,166),fill='#dedcdf',width=2)
 if kind=='confused':
  if t>=.15:bubble(im,(25,215),'I thought you looked confused.',False,30,430)
  if t>=3.4:bubble(im,(182,394),'I was.',True,31,310);txt(im,(342,482),'Seen',19,'#77767a')
 else:
  if t>=.4:bubble(im,(25,210),'Did you arrange this?',False,31,420)
  if t>=4.3:bubble(im,(62,366),'Roy chose the song.',True,31,430)
  if t>=6.35:
   y=540-int(10*(1-ease((t-6.35)/.3)));d.rounded_rectangle((23,y,497,y+118),radius=18,fill='#f7e1e4');txt(im,(55,y+25),'YOU BLOCKED NATHAN',24,'#9e1c2b',True);txt(im,(59,y+66),'You can no longer reply.',23,'#6b454b')
 d.rounded_rectangle((22,810,498,875),radius=30,fill='#efedef');txt(im,(47,829),'Message…',25,'#a09b9f');d.rounded_rectangle((180,900,340,907),radius=4,fill='#171719');return im
def phone(kind,duration,name):
 cache={}
 def fn(t):
  state=(t>=.15,t>=3.4) if kind=='confused' else (t>=.4,t>=4.3,round(min(max(t-6.35,0),.4),2))
  if state not in cache:
   im=Image.new('RGB',(W,H),'#242328');d=ImageDraw.Draw(im);d.rounded_rectangle((430,3,850,719),radius=52,fill='#080809',outline='#626067',width=3);ui=phone_ui(kind,t).resize((394,697),Image.Resampling.LANCZOS);mask=Image.new('L',ui.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,*ui.size),radius=36,fill=255);im.paste(ui,(443,11),mask);d.rounded_rectangle((568,17,712,40),radius=12,fill='#0a090a');txt(im,(50,55),'PINTEREST',23,'#e9e5e2',True);txt(im,(50,90),'Direct messages',20,'#a19c9f');cache[state]=im
  return cache[state]
 encode(OUT/name,duration,fn)
def dm_pairs():
 phone('confused',6,'confused-dm.mp4');phone('arranged',8,'arranged-dm.mp4')
 for n,file,ss,dur in [('T08','confused-dm.mp4',0,3),('T09','confused-dm.mp4',3,3),('T25','arranged-dm.mp4',0,4),('T26','arranged-dm.mp4',4,4)]:ff(['-ss',ss,'-i',OUT/file,'-t',dur,'-an','-c:v','libx264','-crf',18,'-preset','fast',OUT/'segments'/f'{n}.mp4'])
def editing_board(live,letter):
 im=Image.new('RGB',(W,H),'#182024');d=ImageDraw.Draw(im);txt(im,(27,18),'DOCUMENTARY / CASTING / ROY',24,'#e9e5dc',True);txt(im,(1010,22),'SELECTS / 03',18,'#bbc0bd');im.paste(Image.fromarray(live).resize((800,450),Image.Resampling.LANCZOS),(25,70));txt(im,(850,100),'CANDIDATE '+letter,23,'#e9e5dc',True);txt(im,(850,152),'PLAYING',22,'#ccad80');txt(im,(850,220),'Take 01',20,'#c6cdcc');txt(im,(850,262),'Take 02',20,'#c6cdcc');txt(im,(850,304),'Take 03',20,'#c6cdcc')
 for j,l in enumerate(['A','B','C']):
  thumb=Image.open(OUT/'plates'/f'candidate-{l}.jpg');im.paste(thumb.resize((250,141)),(25+j*272,545));txt(im,(30+j*272,661),'ROY / '+l,18,'#e9e5dc')
 return np.array(im)
def auditions():
 background=np.array(Image.open(HERE/'images/macbook.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS));corners=np.float32([[405/1672*W,96/940*H],[1273/1672*W,99/940*H],[1290/1672*W,620/940*H],[376/1672*W,619/940*H]])
 for letter in 'ABC':
  fs=readframes(RAW/f'candidate_{letter.lower()}.mp4',0,1);Image.fromarray(fs[12]).save(OUT/'plates'/f'candidate-{letter}.jpg')
 for n,letter,dur in [('T11','A',4),('T12','B',4),('T13','C',6)]:
  # Use the accepted speaking performance at screen scale; playback remains moving, never a held portrait.
  live=readframes(ROOT/'build/first-trailer-finishing-d4/segments'/f'{n}.mp4',0,dur)
  def fn(t):
   shot=Image.fromarray(get(live,t));ImageDraw.Draw(shot).rectangle((0,0,240,42),fill='#11171a');txt(shot,(12,12),'CANDIDATE '+letter+' / TAKE 01',16,'#ddd',True);shot=np.array(shot);ui=editing_board(shot,letter);scene=composite_screen(background,ui,corners,.13)
   # Screen reflections come from the photographed display and stay locked to the physical glass.
   if n=='T11':
    video_rect=np.float32([[25,70],[825,70],[825,520],[25,520]]);video_world=project(cv2.getPerspectiveTransform(quad(),corners),video_rect);u=ease((t-1.6)/2.0);vp=video_world*(1-u)+quad()*u;return view(scene,vp)
   return scene
  encode(OUT/'segments'/f'{n}.mp4',dur,fn);print(n,'moving MacBook audition',flush=True)
def post_base(author,caption):
 im=Image.new('RGB',(W,H),'#f5f2ec');d=ImageDraw.Draw(im);d.rectangle((0,0,W,56),fill='white');d.ellipse((24,10,59,45),fill='#bc2131');txt(im,(34,14),'P',23,'white',True);txt(im,(84,17),'Pinterest',22,bold=True);d.rounded_rectangle((277,10,1040,44),radius=18,fill='#edebea');txt(im,(300,15),'Search',20,'#888');txt(im,(45,78),author,27,bold=True);txt(im,(45,119),caption,27);return im
def angry(im,xy,count):
 d=ImageDraw.Draw(im);x,y=xy;d.ellipse((x,y,x+48,y+48),fill='#df6a49');d.line((x+9,y+13,x+21,y+18),fill='#58291f',width=3);d.line((x+28,y+18,x+39,y+13),fill='#58291f',width=3);d.ellipse((x+14,y+21,x+18,y+25),fill='#58291f');d.ellipse((x+31,y+21,x+35,y+25),fill='#58291f');d.arc((x+15,y+30,x+35,y+46),180,350,fill='#58291f',width=3);txt(im,(x+65,y+6),count,33,'#ba2934',True)
def small_reactions(im):
 d=ImageDraw.Draw(im)
 # Native reaction icons avoid missing emoji-font glyphs.
 points=[]
 for v in np.linspace(0,2*np.pi,80):points.append((74+1.4*16*np.sin(v)**3,652-1.4*(13*np.cos(v)-5*np.cos(2*v)-2*np.cos(3*v)-np.cos(4*v))))
 d.polygon(points,fill='#b93c4f');txt(im,(112,636),'23',27,'#74716f')
 for x,kind,count in [(205,'laugh','86'),(359,'surprise','4')]:
  y=628;d.ellipse((x,y,x+48,y+48),fill='#efb850');d.ellipse((x+12,y+13,x+17,y+19),fill='#573d25');d.ellipse((x+31,y+13,x+36,y+19),fill='#573d25')
  if kind=='laugh':d.pieslice((x+10,y+18,x+39,y+42),0,180,fill='#633a2d');d.line((x+12,y+29,x+36,y+29),fill='white',width=3)
  else:d.ellipse((x+18,y+26,x+30,y+42),fill='#633a2d')
  txt(im,(x+64,636),count,27,'#74716f')
def trolling_post():
 live=readframes(RAW/'lodge.mp4',6,6);base=post_base('Dan · CEO, Pinterest','I’d like the conversation to happen on Pinterest.');d=ImageDraw.Draw(base);d.rectangle((45,163,835,609),fill='black');txt(base,(868,190),'The conversation',28,bold=True);txt(base,(868,230),'is happening.',28,bold=True);txt(base,(868,320),'Saved by Dan',23,'#777');small_reactions(base);angry(base,(560,628),'9,999,999,999+')
 def fn(t):
  im=base.copy();im.paste(Image.fromarray(get(live,t)).resize((790,444),Image.Resampling.LANCZOS),(45,164));return im
 encode(OUT/'segments/T22.mp4',6,fn)
def nathan_post():
 live=readframes(D7/'segments/T28.mp4',0,6);base=post_base('Nathan','I didn’t know.');rect=np.float32([[180,170],[1100,170],[1100,688],[180,688]])
 def fn(t):
  im=base.copy();im.paste(Image.fromarray(get(live,t)).resize((920,518),Image.Resampling.LANCZOS),(180,170));u=ease((t-1.8)/2.5);vp=rect*(1-u)+quad()*u;return view(np.array(im),vp)
 encode(OUT/'segments/T28.mp4',6,fn)
def lawyer_dm():
 im=Image.new('RGB',(W,H),'#faf9f7');d=ImageDraw.Draw(im);d.rectangle((0,0,W,100),fill='#f0edeb');txt(im,(48,24),'PINTEREST / MESSAGES',21,'#9b2031',True);txt(im,(48,57),'Roy  ↔  Lawyer',30,bold=True);txt(im,(910,43),'Private conversation',23,'#777');bubble(im,(55,155),'Did you authorize this?',False,34,620);bubble(im,(354,326),'I didn’t know they were going to use—',True,38,850);txt(im,(1015,535),'Delivered',22,'#777');return np.array(im)
def billboard():
 base=np.array(Image.open(HERE/'images/times_square.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS));dst=np.float32([[402/1672*W,100/940*H],[1270/1672*W,35/940*H],[1297/1672*W,585/940*H],[370/1672*W,600/940*H]]);ui=lawyer_dm();scene=composite_screen(base,ui,dst,.015)
 def fn(t):
  u=ease((t-2)/2);vp=dst*(1-u)+quad()*u;return view(scene,vp)
 encode(OUT/'segments/T36.mp4',6,fn)
def picture():
 init();special={'T04','T05','T06','T07','T08','T09','T11','T12','T13','T22','T25','T26','T28','T36'};sources=[]
 for r in rows():
  n=r['segment'];dur=float(r['duration_seconds']);target=OUT/'segments'/f'{n}.mp4'
  if target.exists():continue
  if n in ['T03','T10','T15','T21','C04']:still(n,card(n),dur);kind='requested static title / exact replacement handle'
  elif n=='T18':still(n,Image.open(HERE/'images/plan.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS),dur);kind='friendly planning rendering'
  elif n in special:continue
  else:shutil.copy2(D7/'segments'/f'{n}.mp4',target);kind='preserved accepted D7 composition'
  sources.append({'segment':n,'kind':kind})
 if not (OUT/'segments/T04.mp4').exists():split_takes()
 if not (OUT/'segments/T08.mp4').exists():dm_pairs()
 if not (OUT/'segments/T11.mp4').exists():auditions()
 if not (OUT/'segments/T22.mp4').exists():trolling_post()
 if not (OUT/'segments/T28.mp4').exists():nathan_post()
 if not (OUT/'segments/T36.mp4').exists():billboard()
 for r in rows():assert (OUT/'segments'/f"{r['segment']}.mp4").exists(),r
 put(OUT/'picture-sources.json',sources);(OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in rows()));ff(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4']);print('D8 picture assembled',flush=True)
def export():
 style='FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48'
 ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',f"subtitles={OUT/'captions.srt'}:fontsdir={FONT.parent}:force_style='{style}'",'-map','0:v','-map','1:a','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar',48000,'-t',DUR,'-metadata','title=YOU CAN SEE EVERYTHING - D8 user editorial revision','-movflags','+faststart',OUT/'first-trailer-revision-d8.mp4']);print('D8 exported',flush=True)
def remaster_export():
 p=OUT/'first-trailer-revision-d8.mp4';tmp=OUT/'first-trailer-revision-d8-remix.mp4'
 ff(['-i',p,'-i',OUT/'mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-ar',48000,'-t',DUR,'-movflags','+faststart',tmp]);tmp.replace(p)
if __name__=='__main__':
 for name in sys.argv[1:]:globals()[name]()
