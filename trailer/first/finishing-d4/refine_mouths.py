"""Narrow the restored region to lips/jaw, retaining original nose/cheek texture."""
from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np,cv2
sys.path.insert(0,str(Path(__file__).resolve().parent))
from lipsync import Engine,reader
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-finishing-d4'
engine=Engine()
names=['T04','T02','T07','T08','T09','T10_fielder','T10_dan','T11','T12','T13','T15','T18','T22','T23','T25','T26','T27','T28','T30','T31','T35','T39_T40']
if len(sys.argv)>1:names=[x for x in names if x in sys.argv[1:]]
for name in names:
 raw=OUT/'synced'/(name+'.mp4');metadata=raw.with_suffix('.json')
 if not metadata.exists():continue
 output=OUT/'polished'/(name+'.mp4');output.parent.mkdir(parents=True,exist_ok=True)
 if output.exists() and output.with_suffix('.json').exists():continue
 info=json.loads(metadata.read_text());source=ROOT/info['source'] if not Path(info['source']).is_absolute() else Path(info['source'])
 if name=='T10_dan':source=OUT/'polished/T10_fielder.mp4'
 frames=reader(source);bounds,valid,total=engine.boxes(frames,info['roi']);h,w=frames[0].shape[:2]
 decoded=cv2.VideoCapture(str(raw));proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',str(output)],stdin=subprocess.PIPE)
 for f,(x1,y1,x2,y2) in zip(frames,bounds):
  okay,synced=decoded.read();assert okay
  rh,rw=y2-y1,x2-x1;yy,xx=np.mgrid[:rh,:rw]
  radius=np.sqrt(((xx/(rw-1)-.5)/.35)**2+((yy/(rh-1)-.77)/.18)**2)
  mask=np.clip((1-radius)/.22,0,1)[:,:,None]
  base=f[y1:y2,x1:x2].astype(float);patch=synced[y1:y2,x1:x2].astype(float)
  f[y1:y2,x1:x2]=np.clip(base*(1-mask)+patch*mask,0,255).astype(np.uint8);proc.stdin.write(f.tobytes())
 proc.stdin.close();assert proc.wait()==0;decoded.release()
 np.save(output.with_suffix('.face-boxes.npy'),bounds)
 info.update({'composite_source':str(source),'refined_output':str(output),'refinement':'Narrow lip/jaw feather; original nose and cheek texture restored','sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'face_boxes':str(output.with_suffix('.face-boxes.npy'))})
 output.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n');print('Refined',name,flush=True)
