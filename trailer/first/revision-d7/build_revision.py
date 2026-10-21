"""D7: native performances, editorial coverage and continuous audible diegetic uke."""
from pathlib import Path
import csv,json,hashlib,importlib.util,shutil,subprocess,sys,math
import numpy as np,soundfile as sf,cv2
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');HERE=ROOT/'trailer/first/revision-d7';OUT=ROOT/'build/first-trailer-revision-d7';D6=ROOT/'build/first-trailer-revision-d6';D3=ROOT/'build/first-trailer-picture-pass-d3';RAW=ROOT/'clips/first/picture-pass-d3'
spec=importlib.util.spec_from_file_location('d6',ROOT/'trailer/first/revision-d6/build_revision.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
SR=48000;N=191*SR;W=1280;H=720;FONT=b.FONT;REG=b.REGULAR
def ff(args):return b.ff(args)
def put(p,v):b.put(p,v)
def init():
 for n in ['segments','stems','plates','contacts','score','audio-review','pdf-review']: (OUT/n).mkdir(parents=True,exist_ok=True)
def prepare():
 init();(OUT/'speech').mkdir(exist_ok=True);shutil.copy2(D6/'timeline.csv',OUT/'timeline.csv')
 timing=json.loads((D6/'speech/timing.json').read_text());lines=list(csv.DictReader((D6/'dialogue.csv').open()))
 for f in (D6/'speech').glob('L*.wav'):shutil.copy2(f,OUT/'speech'/f.name)
 e=next(x for x in timing if x['id']=='L29');delta=161.3-e['start'];e['start']=161.3;e['actual_end']+=delta;e['target_end']=163.55;e['caption_end']=163.55
 row=next(x for x in lines if x['line_id']=='L29');row.update(start_seconds=161.3,end_seconds=163.55,source='reuse dialogue/v2/d03.mp3; delivered visibly by Dan in T35')
 put(OUT/'speech/timing.json',timing)
 with (OUT/'dialogue.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(lines[0]));w.writeheader();w.writerows(lines)
 (OUT/'captions.srt').write_text('\n\n'.join(f"{i}\n{b.stamp(e['start'])} --> {b.stamp(e['caption_end'])}\n{next(x['text'] for x in lines if x['line_id']==e['id'])}" for i,e in enumerate(timing,1))+'\n')
 put(OUT/'edit-plan.json',{'duration':191,'segments':44,'minimum_hold':2,'source':'D6 durations retained in full','changes':['T35 visibly Dan; L29 audio starts 161.3 and ends 162.993, caption ends 163.55 before Roy at 164','Stationary still character plus stationary performance driver, expressiveness 1, gestures off; final native output used directly','Candidate audio-review filmstrip, rear interview and comms coverage, instrument inserts, paused stream','Roy strums from first frame through 18; final diegetic strums 177-187; CTA silent'],'RULES.md':'All 44 holds retain D6 durations; no shot shortened. Full-trailer changes explicitly requested by user; accepted words/voice files preserved. Final actual artifact is checked, including segment audit.'})
def compose():
 init();d=json.loads((D6/'score/events.json').read_text());ev=d['events'];ev['roy']=[e for e in ev['roy'] if 18<=e['t']<177]
 chords=[[57,60,64,69],[55,59,64,67],[55,60,64,67],[55,59,64,67]]
 for lo,hi,mode in [(0,8,'ringing'),(8,12,'palm-muted'),(12,18,'ringing'),(108,114,'quiet intro'),(177,187,'room only')]:
  for i,t in enumerate(np.arange(lo,hi,.5)):
   notes=[57,61,64,69] if lo==0 and t>=7 else chords[(i//2)%4]
   ev['roy'].append({'t':float(t),'d':.5,'notes':notes,'v':55 if mode in ['palm-muted','quiet intro'] else 76 if i%2==0 else 66,'articulation':mode,'source_staff':'diegetic four-string strum, strings staggered 13ms'})
 ev['roy'].sort(key=lambda e:e['t']);d.update(version='D7 continuous diegetic ukulele',gates=[[171,173],[187,191]],opening='Audible 0-18 including palm-muted apology; quiet intro 108-114; retained middle 114-130.',ending='Non-diegetic score ends 177. Roy plays in room 177-187, including question and notification. CTA 187-191 silent.')
 put(OUT/'score/events.json',d)
 with (OUT/'score/event-cues.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['role','onset_seconds','release_seconds','notes','velocity','articulation'])
  for role,es in ev.items():
   for e in es:w.writerow([role,e['t'],e['t']+e['d'],' '.join(map(str,e['notes'])),e['v'],e.get('articulation','')])
def strum(e):
 muted=e.get('articulation')=='palm-muted';length=.38 if muted else 1.5
 if e['t']<18:length=min(length,18-e['t'])
 elif 108<=e['t']<114:length=min(length,114-e['t'])
 z=np.zeros(round(length*SR),np.float32)
 for j,n in enumerate(e['notes']):
  a=b.b.sample(n);a=b.b.envelope(a,.003,.05)*np.exp(-np.arange(len(a))/SR/(.16 if muted else .85));a/=max(abs(a));start=round(j*.013*SR);count=min(len(a),len(z)-start)
  z[start:start+count]+=a[:count]
 z=b.b.envelope(z,.003,.045);z/=max(abs(z));amp={'ringing':.24,'palm-muted':.24,'quiet intro':.24,'room only':.22}[e['articulation']]
 return b.b.stereo(z*(amp if e['v']>=70 else amp*.79))
def audio():
 init();ev=json.loads((OUT/'score/events.json').read_text())['events'];timing=json.loads((OUT/'speech/timing.json').read_text());roy=b.read(D6/'stems/roy.wav');roy[:18*SR]=0;roy[177*SR:]=0
 for e in ev['roy']:
  if 'articulation' in e and (e['t']<18 or 108<=e['t']<114 or e['t']>=177):b.add(roy,strum(e),e['t'])
 duck=np.ones(N,np.float32)
 for e in timing:duck[max(0,round((e['start']-.04)*SR)):round((e['actual_end']+.10)*SR)]=.65
 idx=np.arange(0,N,240);coarse=duck[idx]
 for _ in range(4):coarse=np.convolve(coarse,[.2,.6,.2],mode='same')
 duck=np.interp(np.arange(N),idx,coarse).astype(np.float32)
 for lo,hi in [(0,18),(108,114),(177,187)]:roy[lo*SR:hi*SR]*=(np.maximum(duck[lo*SR:hi*SR],.82) if lo==177 else duck[lo*SR:hi*SR])[:,None]
 roy[round(17.94*SR):18*SR]*=np.linspace(1,0,round(.06*SR))[:,None];roy[round(186.9*SR):187*SR]*=np.linspace(1,0,round(.1*SR))[:,None];roy[187*SR:]=0;b.save(OUT/'stems/roy.wav',roy);music=roy.copy()
 for role in ['plucks','low','bloom','grit','body','reverse']:
  shutil.copy2(D6/'stems'/f'{role}.wav',OUT/'stems'/f'{role}.wav');music+=b.read(OUT/'stems'/f'{role}.wav')
 b.save(OUT/'music-only.wav',music);dialogue=b.read(D6/'stems/dialogue.wav');old=next(x for x in json.loads((D6/'speech/timing.json').read_text()) if x['id']=='L29');new=next(x for x in timing if x['id']=='L29');z=b.b.stereo(b.rawmono(OUT/'speech/L29.wav'));i=round(old['start']*SR);dialogue[i:i+len(z)]-=z;b.add(dialogue,z,new['start']);b.save(OUT/'stems/dialogue.wav',dialogue);mix=music+dialogue
 for role in ['effects','ambience']:
  shutil.copy2(D6/'stems'/f'{role}.wav',OUT/'stems'/f'{role}.wav');mix+=b.read(OUT/'stems'/f'{role}.wav')
 mix[171*SR:173*SR]=0;b.save(OUT/'premaster.wav',mix);before=b.b.loudness(OUT/'premaster.wav');gain=-18-float(before['input_i'])
 ff(['-i',OUT/'premaster.wav','-af',f'volume={gain}dB,aresample=192000,alimiter=limit=0.84:attack=5:release=80:level=false:latency=true,aresample=48000','-c:a','pcm_f32le',OUT/'master-limited.wav'])
 master=b.read(OUT/'master-limited.wav')[:N];master[171*SR:173*SR]=0;master[187*SR:]=0;b.save(OUT/'mix.wav',master);after=b.b.loudness(OUT/'mix.wav');put(OUT/'mix.json',{'master_gain_db':gain,'premaster_loudness':before,'master_loudness':after,'dialogue':'All accepted speech PCM preserved. L29 moved to 161.3 on Dan.','diegetic_uke_windows':[[0,18],[108,130],[177,187]],'score_ends':177,'silence':[[171,173],[187,191]],'other_stems':'D6 byte-identical'})
 for start,dur,name in [(0,26,'opening'),(158,33,'ending')]:ff(['-ss',start,'-i',OUT/'mix.wav','-t',dur,'-c:a','libmp3lame','-b:a','192k',OUT/'audio-review'/f'{name}.mp3'])
 print('D7 audio',after,flush=True)
def text(d,xy,s,size=22,fill='#e2ded3',bold=False):d.text(xy,s,font=ImageFont.truetype(str(FONT if bold else REG),size),fill=fill)
def frame(path,t=0):
 c=cv2.VideoCapture(str(path));c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,z=c.read();c.release();assert ok,(path,t);return Image.fromarray(cv2.cvtColor(z,cv2.COLOR_BGR2RGB))
def review(name,duration):
 # One held composition; audio review marker and sharp stationary photographs.
 if name in ['T11','T12','T13']:
  letter={'T11':'A','T12':'B','T13':'C'}[name];source=RAW/f'candidate_{letter.lower()}.mp4';title='CASTING / ROY';label=f'CANDIDATE {letter}';times=[.5,1.5,2.5];main=frame(source,1.5);thumbs=[frame(source,t) for t in times];audio=b.rawmono(OUT/'speech'/f"L{int(name[1:]):02}.wav");playing=True
 elif name=='T31':
  source=RAW/'roy_continuous.mp4';title='STREAM REVIEW';label='ROY / ORIGINAL UPLOAD';main=frame(source,2);thumbs=[main]*3;audio=np.zeros(10);playing=False
 else:
  source=RAW/'fielder_practice.mp4';title='REACTION SELECTS';label='FIELDER / REHEARSAL';main=frame(D3/'segments/T05.mp4',1.1);thumbs=[frame(D3/'segments/T05.mp4',1.1),frame(source,3),frame(source,8)];audio=np.zeros(10);playing=False
 im=Image.new('RGB',(W,H),'#101618');d=ImageDraw.Draw(im);d.rectangle((0,0,1280,55),fill='#232d30');text(d,(30,16),'DOCUMENTARY / '+title,20,bold=True);text(d,(1010,20),'SELECTS  /  03',16)
 im.paste(ImageOps.fit(main,(775,436)),(30,75));text(d,(840,94),label,22,bold=True);text(d,(840,140),'AUDIO PLAYBACK' if playing else 'PAUSED',20,fill='#dfae70');text(d,(840,188),'01   Original interview',18);text(d,(840,226),'02   Rehearsal',18);text(d,(840,264),'03   Rehearsal',18)
 for j,thumb in enumerate(thumbs):
  x=30+j*260;im.paste(ImageOps.fit(thumb,(248,139)),(x,527));d.rectangle((x,527,x+248,666),outline='#59666a',width=1);text(d,(x+8,639),f'TAKE {j+1:02}',16)
 d.rectangle((839,340,1240,505),fill='#182226');text(d,(854,354),'RECORDING' if playing else 'PICTURE SELECT',16)
 if playing:
  edges=np.linspace(0,len(audio),170).astype(int);peak=max(abs(audio))
  for j in range(169):
   h=max(1,int(np.max(abs(audio[edges[j]:edges[j+1]]))/peak*38));x=855+j*2.2;d.line((x,440-h,x,440+h),fill='#8cbab1',width=1)
 else:text(d,(854,422),'SOURCE / REVIEW COPY',17)
 p=OUT/'plates'/f'{name}.png';im.save(p);vf="drawbox=x='855+365*t/%s':y=395:w=2:h=96:color=0xd3a770:t=fill"%duration if playing else 'null'
 ff(['-loop','1','-framerate',24,'-i',p,'-t',duration,'-vf',vf,'-an','-c:v','libx264','-crf',17,'-preset','fast','-pix_fmt','yuv420p',OUT/'segments'/f'{name}.mp4']);return source
def still(source,target,dur,push=True):
 vf='scale=1320:744:force_original_aspect_ratio=increase,crop=1320:744,zoompan=z=1.01+0.00012*on:x=iw/2-iw/zoom/2:y=ih/2-ih/zoom/2:d=1:s=1280x720:fps=24' if push else 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720'
 ff(['-loop','1','-framerate',24,'-i',source,'-t',dur,'-vf',vf,'-an','-c:v','libx264','-crf',17,'-preset','fast','-pix_fmt','yuv420p',target])
def picture():
 init();rows=list(csv.DictReader((OUT/'timeline.csv').open()));sources=[]
 jobs={x['segment']:(j['key'],x['offset']) for j in json.loads((OUT/'drivers/jobs.json').read_text()) for x in j['segments']};jobs['T04']=('dan-test',0)
 for r in rows:
  n=r['segment'];dur=float(r['duration_seconds']);target=OUT/'segments'/f'{n}.mp4';source=D6/'segments'/f'{n}.mp4';kind='preserved D6 composition'
  if target.exists():continue
  if n in jobs:
   key,offset=jobs[n];source=OUT/'performance'/f'{key}-native.mp4';assert source.exists(),source
   timing=json.loads((OUT/'speech/timing.json').read_text());onset=float(r['start_seconds']);last=max(e['actual_end'] for e in timing if onset<=e['start']<onset+dur);live=min(dur,math.ceil((last-onset+.10)*24)/24)
   vf=f'trim=duration={live},setpts=PTS-STARTPTS,fps=24,tpad=stop_mode=clone:stop_duration={dur},scale=1280:720'
   if n in ['T04','T35']:vf+=f",drawbox=x=38:y=539:w=264:h=64:color=black@0.62:t=fill,drawtext=fontfile={FONT}:text='DAN':fontsize=24:fontcolor=white:x=52:y=548,drawtext=fontfile={REG}:text='CEO / Pinterest':fontsize=18:fontcolor=white:x=52:y=577"
   ff(['-ss',offset,'-i',source,'-t',dur,'-vf',vf,'-an','-c:v','libx264','-crf',17,'-preset','fast','-pix_fmt','yuv420p',target]);kind='Native sharp stationary Act-Two output; whole frame held after speech plus 100ms; no mouth patch'
  elif n in ['T10','T15','T18']:
   source=HERE/'images'/('T10-reverse.png' if n=='T10' else 'communications-reverse.png');still(source,target,dur);kind='Reverse-angle interview coverage'
  elif n in ['T11','T12','T13','T31','T34']:source=review(n,dur);kind='Held sharp contact-sheet / audio review composition'
  elif n in ['T02','T03','T23','T27','T39','T40']:
   raw,offset={'T02':('roy_end',2),'T03':('roy_continuous',0),'T23':('roy_continuous',0),'T27':('candidate_uke',0),'T39':('roy_end',0),'T40':('roy_end',5)}[n];source=RAW/f'{raw}.mp4'
   vf='fps=24,scale=1280:720,crop=900:330:230:390,scale=1280:470,pad=1280:720:0:125:black'
   if n=='T40':vf+=f",drawbox=x=810:y=26:w=430:h=84:color=0xf0ede5:t=fill,drawtext=fontfile={FONT}:text='PINTEREST':fontsize=18:fontcolor=0x9a1d2d:x=830:y=40,drawtext=fontfile={REG}:text='We hear you, Roy.':fontsize=25:fontcolor=0x191919:x=830:y=69"
   ff(['-ss',offset,'-i',source,'-t',dur,'-vf',vf,'-an','-c:v','libx264','-crf',17,'-preset','fast','-pix_fmt','yuv420p',target]);kind='Native instrument insert; face outside frame'
  elif n in ['T25','T28','T36']:
   source=D3/'segments'/f'{n}.mp4';p=OUT/'plates'/f'{n}.png';im=frame(source,1)
   if n=='T36':im=im.crop((630,250,1280,680)).resize((1088,720),Image.Resampling.LANCZOS);base=Image.new('RGB',(1280,720),'black');base.paste(im,(96,0));im=base
   # Replace the old production badge with matching unobtrusive review metadata.
   d=ImageDraw.Draw(im);d.rectangle((0,0,240,42),fill='#0a1012');text(d,(12,12),'REVIEW / SOURCE RECORDING',14);im.save(p);still(p,target,dur,False);kind='Sharp held monitor coverage; off-screen voice'
  elif n in ['T01','T24']:
   source=D3/'segments'/f'{n}.mp4';ff(['-i',source,'-t',dur,'-vf',f"drawbox=x=0:y=0:w=240:h=42:color=0x0a1012:t=fill,drawtext=fontfile={REG}:text='STREAM / ROY':fontsize=15:fontcolor=white:x=12:y=12",'-an','-c:v','libx264','-crf',17,'-preset','fast','-pix_fmt','yuv420p',target]);kind='Clean native Roy performance; no local mouth patch'
  else:shutil.copy2(source,target)
  sources.append({'segment':n,'source':str(source),'kind':kind,'duration':dur});print(n,kind,flush=True)
 old=json.loads((OUT/'picture-sources.json').read_text()) if (OUT/'picture-sources.json').exists() else []
 put(OUT/'picture-sources.json',old+sources);(OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in rows));ff(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4'])
def localpicture():
 # Render independent coverage while the remote performances are generating.
 jobs={'T04','T07','T08','T09','T22','T26','T30','T35'};p=OUT/'timeline.csv';original=p.read_text();rows=list(csv.DictReader(p.open()))
 try:
  with p.open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(r for r in rows if r['segment'] not in jobs)
  picture()
 finally:p.write_text(original)
def score():
 # Same open-source score adapter, corrected diegetic ending and version labels.
 code=(ROOT/'trailer/first/revision-d6/build_revision.py').read_text();code=code.replace('D6 - ukulele score / editorial revision','D7 - ukulele score / continuous room performance').replace('177:\'Roy / room only\'','177:\'Roy / diegetic strums\'').replace('no music after 2:57.','score ends 2:57; Roy plays to 3:07; CTA silent.').replace('ukulele-score-d6','ukulele-score-d7')
 ns=dict(b.__dict__);exec(compile(code,str(HERE/'score-adapter.py'),'exec'),ns);ns['OUT']=OUT;ns['HERE']=HERE;ns['score']()
def export():
 b.OUT=OUT
 style='FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48'
 ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',f"subtitles={OUT/'captions.srt'}:fontsdir={FONT.parent}:force_style='{style}'",'-map','0:v','-map','1:a','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar',SR,'-t',191,'-metadata','title=YOU CAN SEE EVERYTHING - D7 performance and editorial revision','-movflags','+faststart',OUT/'first-trailer-revision-d7.mp4']);print('D7 exported',flush=True)
def remaster_export():
 p=OUT/'first-trailer-revision-d7.mp4';temp=OUT/'first-trailer-revision-d7-remix.mp4'
 ff(['-i',p,'-i',OUT/'mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-ar',48000,'-t',191,'-movflags','+faststart',temp]);temp.replace(p)
if __name__=='__main__':
 for name in sys.argv[1:]:globals()[name]()
