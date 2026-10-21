"""Stationary performance drivers: voice timing without inherited head nods."""
from pathlib import Path
import csv,json,sys,subprocess,hashlib
import cv2,numpy as np,soundfile as sf
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-revision-d7';D6=ROOT/'build/first-trailer-revision-d6';MEDIA=ROOT/'clips/first/picture-pass-d3'
sys.path.insert(0,str(ROOT/'trailer/first/finishing-d4'));from lipsync import Engine,load_audio
ROWS={x['segment']:x for x in csv.DictReader((D6/'timeline.csv').open())};TIMING=json.loads((OUT/'speech/timing.json').read_text())
JOBS=[
 ('dan-main','DAN', [('T08',3),('T22',6),('T26',4),('T30',3),('T35',3)],'dan',5,None),
 ('fielder-main','FIELDER',[('T07',4),('T09',3)],'fielder_practice',8,None),
 ('roy-main','ROY',[('T02',4),('T23',6),('T39',5),('T40',5)],'roy_end',0,None),
 ('candidate-a','ROY CANDIDATE A',[('T11',4)],'candidate_a',3,None),
 ('candidate-a-uke','ROY CANDIDATE A',[('T27',6)],'candidate_uke',3,None),
 ('candidate-b','ROY CANDIDATE B',[('T12',4)],'candidate_b',3,None),
 ('candidate-c','ROY CANDIDATE C',[('T13',6)],'candidate_c',4,None),
 ('communications','COMMUNICATIONS',[('T15',5),('T18',3)],'communications',5,None),
 ('table-dan','DAN',[('T10',8)],'table',0,'left'),
 ('table-fielder','FIELDER',[('T10',8)],'table',0,'right'),
]
def ff(args):subprocess.run(['ffmpeg','-y','-v','error',*map(str,args)],check=True)
engine=Engine();ledger=[]
for key,role,segments,asset,ss,half in JOBS:
 if len(sys.argv)>1 and key not in sys.argv[1:]:continue
 folder=OUT/'drivers';folder.mkdir(parents=True,exist_ok=True);image=folder/f'{key}-character.png';duration=sum(d for _,d in segments);video=folder/f'{key}-still.mp4';audio=folder/f'{key}.wav';driver=folder/f'{key}-driver.mp4';synced=folder/f'{key}-mouth.mp4'
 vf='scale=1280:720'
 if half:vf+=f',crop=640:720:{0 if half=="left" else 640}:0,pad=720:720:40:0:black'
 ff(['-ss',ss,'-i',MEDIA/f'{asset}.mp4','-frames:v',1,'-vf',vf,image])
 a=np.zeros(round(duration*16000),np.float32);cursor=0;pieces=[]
 for segment,d in segments:
  start=float(ROWS[segment]['start_seconds']);pieces.append({'segment':segment,'offset':cursor,'duration':d})
  for line in TIMING:
   if line['speaker']==role and start<=line['start']<start+d:
    z=load_audio(D6/'speech'/f"{line['id']}.wav");i=round((cursor+line['start']-start)*16000);count=min(len(z),len(a)-i);a[i:i+count]+=z[:count]
  cursor+=d
 sf.write(audio,a,16000,subtype='PCM_16')
 if not driver.exists():
  ff(['-loop',1,'-framerate',24,'-i',image,'-t',duration,'-an','-c:v','libx264','-crf',16,'-pix_fmt','yuv420p',video]);engine.render(video,audio,synced)
  ff(['-i',synced,'-i',audio,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',duration,driver])
 item={'key':key,'role':role,'character':str(image),'driver':str(driver),'duration':duration,'segments':pieces,'half':half,'ratio':'1:1' if half else '16:9','source':str(MEDIA/f'{asset}.mp4'),'source_frame_seconds':ss,'method':'Stationary native character frame; existing accepted voice recordings; mouth driver only. Final delivery uses native high-detail performance output directly. No driver mouth patch enters delivery.','settings':{'facial_expressiveness':1,'gestures':False},'driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest()};ledger.append(item);(folder/f'{key}.json').write_text(json.dumps(item,indent=2)+'\n');print('Prepared',key,duration,flush=True)
alljobs=[json.loads((OUT/'drivers'/f'{j[0]}.json').read_text()) for j in JOBS if (OUT/'drivers'/f'{j[0]}.json').exists()];(OUT/'drivers/jobs.json').write_text(json.dumps(alljobs,indent=2)+'\n')
