"""Assemble the approved full picture pass; keep D2-r1 and the teaser immutable."""
from pathlib import Path
import csv,json,subprocess,importlib.util,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser')
HERE=ROOT/'trailer/first/picture-pass-d3';OUT=ROOT/'build/first-trailer-picture-pass-d3'
MEDIA=ROOT/'clips/first/picture-pass-d3';REF=HERE/'refs';V1=ROOT/'trailer/first/visual-tests/v1'
spec=importlib.util.spec_from_file_location('base',ROOT/'trailer/first/build_animatic.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.OUT=OUT
W,H,FPS=1280,720,24
ROWS=list(csv.DictReader((ROOT/'trailer/first/timeline.csv').open()))
LINES=list(csv.DictReader((HERE/'dialogue.csv').open()))
ENC=['-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','24','-an']
for sub in ('plates','segments','speech','stems','score','contacts'):(OUT/sub).mkdir(parents=True,exist_ok=True)
def ff(args):b.ff(args)
def text(im,xy,s,size=24,color='white',bold=False):ImageDraw.Draw(im).text(xy,s,font=b.font(size,bold),fill=color)
def frame(path,t,size=(W,H)):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf',f'scale={size[0]}:{size[1]}','-pix_fmt','rgb24','-f','rawvideo','-'])
 return Image.frombytes('RGB',size,raw)
def tag(im):
 d=ImageDraw.Draw(im);d.rounded_rectangle((12,12,206,40),5,fill=(10,14,18));text(im,(22,18),'PICTURE PASS D3',16,'#dddddd',True);return im
def labelvf():
 return ",drawbox=x=12:y=12:w=194:h=28:color=black@0.65:t=fill,drawtext=fontfile="+str(b.FONTS['Bold'])+":text='PICTURE PASS D3':fontsize=16:fontcolor=white:x=22:y=18"
def still(n,im,tagged=True):
 if tagged:tag(im)
 p=OUT/'plates'/f'{n}.png';im.save(p);row=next(r for r in ROWS if r['segment']==n)
 ff(['-loop','1','-framerate','24','-i',p,'-t',row['duration_seconds'],*ENC,OUT/'segments'/f'{n}.mp4'])
def motion(n,path,ss=0,vf='scale=1280:720',tagged=True):
 row=next(r for r in ROWS if r['segment']==n)
 ff(['-ss',str(ss),'-i',path,'-t',row['duration_seconds'],'-vf',vf+(labelvf() if tagged else ''),*ENC,OUT/'segments'/f'{n}.mp4'])
def quad(w,h):return np.array([[0,0],[w,0],[w,h],[0,h]],float)
def homography(src,dst):
 rows=[];values=[]
 for (x,y),(u,v) in zip(src,dst):
  rows.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);values.extend([u,v])
 return np.append(np.linalg.solve(np.array(rows,float),np.array(values,float)),1).reshape(3,3)
def project(h,p):
 q=np.column_stack([p,np.ones(len(p))])@h.T;return q[:,:2]/q[:,2:]
def warp(im,src,dst):
 h=homography(dst,src).reshape(-1)
 return im.transform((W,H),Image.Transform.PERSPECTIVE,tuple(h[:8]),Image.Resampling.BICUBIC,fillcolor=(0,0,0,0) if im.mode=='RGBA' else (0,0,0))
def encode_frames(path,count,fn):
 proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','24','-i','-',*ENC,str(path)],stdin=subprocess.PIPE)
 try:
  for i in range(count):proc.stdin.write(fn(i).convert('RGB').tobytes())
 finally:proc.stdin.close()
 assert proc.wait()==0
def reveal():
 room=Image.open(V1/'dan-fielder-monitor-clean-v1.png').convert('RGBA');page=Image.open(V1/'pinterest-wrapper-v1.png').convert('RGBA')
 screen=np.array([[51,178],[820,194],[823,608],[42,671]],float)
 viewport=np.array([[130,278],[1310,278],[1310,942],[130,942]],float)
 pagecorners=quad(*page.size);roomcorners=quad(*room.size);royquad=project(homography(pagecorners,screen),viewport)
 decode=subprocess.Popen(['ffmpeg','-v','error','-i',str(MEDIA/'roy_continuous.mp4'),'-vf','scale=1280:720,fps=24','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 def compose(i):
  raw=decode.stdout.read(W*H*3);assert len(raw)==W*H*3
  live=Image.frombytes('RGB',(W,H),raw).convert('RGBA');t=i/24
  if t<6:view=royquad
  elif t<10:
   u=(t-6)/4;u=u*u*(3-2*u);view=royquad*(1-u)+screen*u
  elif t<14:
   u=(t-10)/4;u=u*u*(3-2*u);view=screen*(1-u)+roomcorners*u
  else:view=roomcorners
  cam=homography(view,quad(W,H))
  scene=warp(room,view,quad(W,H));ui=warp(page,pagecorners,project(cam,screen));performer=warp(live,quad(W,H),project(cam,royquad))
  return tag(Image.alpha_composite(Image.alpha_composite(scene,ui),performer).convert('RGB'))
 continuous=OUT/'reveal-continuous.mp4';encode_frames(continuous,18*24,compose);decode.stdout.close();decode.terminate();decode.wait()
 for n,ss in [('T23',0),('T24',6),('T25',14)]:motion(n,continuous,ss,tagged=False)
 (OUT/'reveal-continuity.json').write_text(json.dumps({'source':str(MEDIA/'roy_continuous.mp4'),'source_frames':432,'timeline_start':104,'timeline_end':122,'mapping':'output frame n uses source frame n throughout full screen, Pinterest page, room monitor','segments':['T23','T24','T25'],'screen_corners':screen.tolist(),'stream_viewport':viewport.tolist()},indent=2))
def editing_ui(review=False):
 im=Image.new('RGB',(W,H),'#20262b');d=ImageDraw.Draw(im)
 text(im,(34,35),'DOCUMENTARY / '+('COMMUNICATIONS REVIEW' if review else 'REACTION SELECTS'),24,'#f1eee6',True)
 source=next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4'))
 shots=[frame(OUT/'segments'/f'{n}.mp4',2.7) for n in ['T05','T06','T07']]
 # Use actual rendered practice frames, never invented duplicates.
 im.paste(shots[0].resize((720,405),Image.Resampling.LANCZOS),(34,94))
 d.rounded_rectangle((782,94,1246,499),12,fill='#303a40')
 text(im,(808,120),'Pinterest / Communications' if review else 'PICTURE SELECT',23,'#b8d7c6',True)
 notes=['Keep this in Dan’s own words.','Can this feel less prepared?'] if review else ['01  Original interview','02  Rehearsal','03  Rehearsal']
 for i,s in enumerate(notes):
  for j,line in enumerate(__import__('textwrap').wrap(s,29)):text(im,(808,181+i*94+j*31),line,23,'#e8e6df')
 for i,shot in enumerate(shots):
  x=34+i*404;im.paste(shot.resize((320,180),Image.Resampling.LANCZOS),(x,510));text(im,(x,696),f'TAKE {i+1:02}',18,'#c7cdc8',True)
 return im
def editor_scene(ui):
 room=Image.open(REF/'editor.png').convert('RGBA');screen=np.array([[96,184],[731,188],[733,542],[98,590]],float)
 scale=np.array([W/room.width,H/room.height]);base=room.resize((W,H),Image.Resampling.LANCZOS)
 return Image.alpha_composite(base,warp(ui.convert('RGBA'),quad(W,H),screen*scale)).convert('RGB')
def audio():
 old=ROOT/'build/first-trailer-voice-pass-d2'
 for p in (old/'score').iterdir():
  if p.is_file() and not (OUT/'score'/p.name).exists():shutil.copy2(p,OUT/'score'/p.name)
 b.EVENTS.update(json.loads((OUT/'score/events.json').read_text())['events'])
 dialogue,timing=b.speech(LINES);b.sound(LINES,dialogue)
 assert len(timing)==31 and not any(x['provider']=='macos' for x in timing)
 shutil.copy2(HERE/'dialogue.csv',OUT/'dialogue.csv');shutil.copy2(ROOT/'trailer/first/timeline.csv',OUT/'timeline.csv')
 print('Audio complete: all 31 cues from ElevenLabs or original teaser.',flush=True)
def picture():
 source=next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4'))
 ordinary={
 'T01':('roy-stream',0),'T02':('roy_end',2),'T03':('roy-stream',1),
 'T04':('dan',6),'T07':('fielder_practice',2),'T08':('dan',0),'T09':('fielder_practice',7),
 'T10':('table',0),'T11':('candidate_a',0),'T12':('candidate_b',0),'T13':('candidate_c',0),
 'T15':('communications',0),'T18':('communications',4),'T19':('lodge',0),'T20':('lodge',6),
 'T22':('dan',1),'T26':('dan',4),'T27':('candidate_uke',0),'T30':('dan',7),'T31':('roy_end',5),
 'T35':('candidate_a',5),'T36':('roy_monitor',3)}
 for n,(name,ss) in ordinary.items():
  if (OUT/'segments'/f'{n}.mp4').exists():continue
  if not (MEDIA/(name+'.mp4')).exists():
   print('Waiting for source',n,name,flush=True);continue
  vf='scale=1280:720'
  if n=='T02':vf='scale=1536:864,crop=1280:720:128:35'
  if n=='T04':
   vf+=",drawbox=x=36:y=475:w=274:h=94:color=black@0.55:t=fill,drawtext=fontfile="+str(b.FONTS['Bold'])+":text='DAN':fontsize=26:fontcolor=white:x=52:y=491,drawtext=fontfile="+str(b.FONTS['Regular'])+":text='CEO, Pinterest':fontsize=23:fontcolor=white:x=52:y=530"
  motion(n,MEDIA/(name+'.mp4'),ss,vf);print('Picture',n,flush=True)
 if not (OUT/'segments/T05.mp4').exists():motion('T05',source,2,'scale=1280:1920,crop=1280:720:0:467')
 if not (OUT/'segments/T06.mp4').exists():motion('T06',ROOT/'clips/first/fielder-rehearsal-test-01.mov',3.7)
 for n,glob,ss in [('T16','*food-bank-*',1),('T17','*empty-lot-after-*',2),('T32','*demolition-*',3)]:
  if not (OUT/'segments'/f'{n}.mp4').exists():motion(n,next((ROOT/'clips/inserts').glob(glob+'.mp4')),ss)
 if not (OUT/'segments/T21.mp4').exists() and (MEDIA/'guests.mp4').exists():motion('T21',MEDIA/'guests.mp4',0)
 for n in ['T14','T33']:
  if n=='T33':frame(OUT/'segments/T32.mp4',1).save(OUT/'plates/demolition.jpg')
  if not (OUT/'segments'/f'{n}.mp4').exists():still(n,b.document('prep' if n=='T14' else 'campaign'))
 if not (OUT/'segments/T24.mp4').exists() and (MEDIA/'roy_continuous.mp4').exists():reveal()
 ui=editing_ui()
 for n,im in [('T28',editor_scene(ui)),('T29',editing_ui(True)),('T34',ui)]:
  if not (OUT/'segments'/f'{n}.mp4').exists():still(n,im)
 if not (OUT/'segments/T37.mp4').exists():still('T37',Image.new('RGB',(W,H),'black'),False)
 if not (OUT/'segments/T38.mp4').exists():
  im=Image.new('RGB',(W,H),'black');title='YOU CAN SEE EVERYTHING';box=ImageDraw.Draw(im).textbbox((0,0),title,font=b.font(43));text(im,((W-box[2])/2,333),title,43,'#eeeae2');still('T38',im,False)
 if not (OUT/'segments/T40.mp4').exists():
  # A single source take continues behind the final comment.
  end=MEDIA/'roy_end.mp4'
  motion('T39',end,0)
  decode=subprocess.Popen(['ffmpeg','-v','error','-ss','5','-i',str(end),'-vf','scale=1280:720,fps=24','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
  def closing(i):
   raw=decode.stdout.read(W*H*3);assert len(raw)==W*H*3
   im=Image.frombytes('RGB',(W,H),raw);d=ImageDraw.Draw(im)
   d.rounded_rectangle((55,438,790,538),16,fill='#f5f3eb');text(im,(80,453),'PINTEREST',21,'#b01f2c',True);text(im,(80,487),'We hear you, Roy.',28,'#252c28');return tag(im)
  encode_frames(OUT/'segments/T40.mp4',120,closing);decode.stdout.close();decode.terminate();decode.wait()
 for row in ROWS:assert (OUT/'segments'/f"{row['segment']}.mp4").exists(),row
def export():
 (OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in ROWS))
 ff(['-f','concat','-safe','0','-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4'])
 style="FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48"
 ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',f"subtitles={OUT/'captions.srt'}:fontsdir={b.FONTDIR}:force_style='{style}'",'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-t','180','-movflags','+faststart',OUT/'first-trailer-picture-pass-d3.mp4'])
if __name__=='__main__':
 import sys
 phases=sys.argv[1:] or ['audio','picture','export']
 for name in phases:globals()[name]()
