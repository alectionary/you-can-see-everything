from pathlib import Path
import sys,json,csv,wave,subprocess,shutil
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from lipsync import Engine,load_audio
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');D3=ROOT/'build/first-trailer-picture-pass-d3';OUT=ROOT/'build/first-trailer-finishing-d4'
ROWS={r['segment']:r for r in csv.DictReader((D3/'timeline.csv').open())};LINES=list(csv.DictReader((D3/'dialogue.csv').open()))
jobs=[
 ('T04','DAN',None),('T02','ROY',[360,0,1050,520]),('T07','FIELDER',None),('T08','DAN',None),('T09','FIELDER',None),
 ('T10_fielder','FIELDER',[660,0,1280,720]),('T10_dan','DAN',[0,0,660,720]),
 ('T11','ROY CANDIDATE A',[300,0,1200,720]),('T12','ROY CANDIDATE B',[320,0,1280,720]),('T13','ROY CANDIDATE C',None),
 ('T15','COMMUNICATIONS',[0,0,1020,720]),('T18','COMMUNICATIONS',[0,0,1020,720]),
 ('T22','DAN',None),('T23','ROY',[360,0,1000,500]),('T25','FIELDER',[900,60,1280,650]),('T26','DAN',None),
 ('T27','ROY CANDIDATE A',[200,0,1200,720]),('T28','FIELDER',[820,40,1280,680]),('T30','DAN',None),
 ('T31',None,[360,0,1000,500]),('T35',None,[300,0,1200,720]),('T39_T40','ROY',[360,30,1000,450])]
def audio_for(name,role,start,duration):
 sr=16000;a=np.zeros(round(duration*sr),np.float32)
 for line in LINES:
  if line['speaker']!=role:continue
  t=float(line['start_seconds'])
  if start<=t<start+duration:
   data=load_audio(D3/'speech'/(line['line_id']+'.wav'));idx=round((t-start)*sr);n=min(len(data),len(a)-idx);a[idx:idx+n]+=data[:n]
 path=OUT/'lip-inputs'/(name+'.wav');path.parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
 return path
engine=Engine();reports=[];failed=[]
for name,role,roi in jobs:
 if len(sys.argv)>1 and name not in sys.argv[1:]:continue
 output=OUT/'synced'/f'{name}.mp4'
 if output.exists() and output.with_suffix('.json').exists():reports.append(json.loads(output.with_suffix('.json').read_text()));continue
 if name=='T39_T40':
  start=170;duration=10;source=OUT/'lip-inputs/T39_T40.mp4';concat=OUT/'lip-inputs/end-concat.txt'
  concat.write_text(''.join(f"file '{D3/'segments'/f'{n}.mp4'}'\n" for n in ['T39','T40']))
  subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(source)],check=True)
 else:
  n=name.split('_')[0];row=ROWS[n];start=float(row['start_seconds']);duration=float(row['duration_seconds']);source=D3/'segments'/f'{n}.mp4'
  if name=='T10_dan':source=OUT/'synced/T10_fielder.mp4'
 audio=audio_for(name,role,start,duration)
 try:
  engine.render(source,audio,output,roi);reports.append(json.loads(output.with_suffix('.json').read_text()))
 except Exception as e:
  print('FAILED',name,type(e).__name__,str(e),flush=True);failed.append({'name':name,'error':str(e)})
 (OUT/'lipsync-batch.json').write_text(json.dumps({'completed':reports,'failed':failed,'license':'Wav2Lip personal/noncommercial only','preserved':'Exact 24fps count; original eyes, brow, body, instrument and room; original approved audio unchanged'},indent=2)+'\n')
print('Batch done',len(reports),'complete',len(failed),'failed',flush=True)
