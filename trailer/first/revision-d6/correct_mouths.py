"""Correct Dan's silent mouth motion without freezing eyes, head or body."""
from pathlib import Path
import csv,json,sys,subprocess,hashlib
import cv2,numpy as np
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');OUT=ROOT/'build/first-trailer-revision-d6';D4=ROOT/'build/first-trailer-finishing-d4'
sys.path.insert(0,str(ROOT/'trailer/first/finishing-d4'))
from lipsync import Engine,reader
engine=Engine();rows={r['segment']:r for r in csv.DictReader((OUT/'timeline.csv').open())};timing=json.loads((OUT/'speech/timing.json').read_text())
def speech_weight(t,windows):
 return max([min(np.clip((t-(lo-.04))/.04,0,1),np.clip((hi+.10-t)/.10,0,1)) for lo,hi in windows] or [0])
def ellipse(box,shape):
 h,w=shape;x1,y1,x2,y2=box;rh=y2-y1;rw=x2-x1;yy,xx=np.mgrid[:h,:w]
 cx=.74 if x2<700 else .50;rx=.27 if x2<700 else .31
 r=np.sqrt(((xx-(x1+rw*cx))/(rw*rx))**2+((yy-(y1+rh*.765))/(rh*.115))**2)
 return np.clip((1-r)/.25,0,1).astype(np.float32)
def openness(frame,box):
 x1,y1,x2,y2=box;rw=x2-x1;rh=y2-y1
 crop=frame[round(y1+rh*.70):round(y1+rh*.83),round(x1+rw*.30):round(x1+rw*.70)]
 g=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY);skin=np.median(cv2.cvtColor(frame[y1:y2,x1:x2],cv2.COLOR_BGR2GRAY))
 return float(np.mean(g<skin*.46)+.20*np.mean(g>skin*1.6))
reports=[]
for name in sys.argv[1:] or ['T04','T08','T10','T22','T26','T30']:
 target=OUT/'mouths'/f'{name}.mp4';meta=target.with_suffix('.json')
 if target.exists() and meta.exists():reports.append(json.loads(meta.read_text()));continue
 source=D4/'segments'/f'{name}.mp4';frames=reader(source);h,w=frames[0].shape[:2];roi=[0,0,660,720] if name=='T10' else [0,0,w,h]
 bounds,valid,total=engine.boxes(frames,roi);start=float(rows[name]['start_seconds']);duration=float(rows[name]['duration_seconds'])
 windows=[(e['start']-start,e['actual_end']-start) for e in timing if e['speaker']=='DAN' and start<=e['start']<start+duration]
 assert windows
 weights=np.array([speech_weight(i/24,windows) for i in range(len(frames))]);candidates=list(range(len(frames)))
 reference_index={'T04':42,'T10':0}.get(name,min(candidates,key=lambda i:openness(frames[i],bounds[i])));reference=frames[reference_index];refbox=bounds[reference_index];mask=ellipse(refbox,(h,w));refgray=cv2.cvtColor(reference,cv2.COLOR_BGR2GRAY)
 x1,y1,x2,y2=refbox;rw=x2-x1;rh=y2-y1;featuremask=np.zeros((h,w),np.uint8);featuremask[round(y1+rh*.10):round(y1+rh*.67),round(x1+rw*.12):round(x2-rw*.12)]=255
 points=cv2.goodFeaturesToTrack(refgray,140,.012,5,mask=featuremask)
 synced=None
 if name=='T04':
  syncpath=OUT/'mouths/T04-full-exchange-sync.mp4'
  if not syncpath.exists():engine.render(source,OUT/'lip-inputs/T04.wav',syncpath,roi)
  synced=reader(syncpath);assert len(synced)==len(frames)
 encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
 transforms=[];fallbacks=0
 for i,(frame,box,weight) in enumerate(zip(frames,bounds,weights)):
  if synced is not None:
   m=ellipse(box,(h,w))[:,:,None];frame=np.clip(frame*(1-m)+synced[i]*m,0,255).astype(np.uint8)
  if weight<1:
   bx,by,be,bottom=box;sx=(be-bx)/rw;sy=(bottom-by)/rh;transform=np.array([[sx,0,bx-x1*sx],[0,sy,by-y1*sy]],np.float32)
   if points is not None:
    moved,okay,error=cv2.calcOpticalFlowPyrLK(refgray,cv2.cvtColor(frames[i],cv2.COLOR_BGR2GRAY),points,None,winSize=(31,31),maxLevel=4)
    good=(okay[:,0]==1)&(error[:,0]<22)
    if np.count_nonzero(good)>=8:
     affine,inliers=cv2.estimateAffinePartial2D(points[good],moved[good],method=cv2.RANSAC,ransacReprojThreshold=2.5)
     if affine is not None and abs(affine[0,1])<.22 and .65<affine[0,0]<1.4:transform=affine.astype(np.float32)
     else:fallbacks+=1
    else:fallbacks+=1
   refwarp=cv2.warpAffine(reference,transform,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
   m=cv2.warpAffine(mask,transform,(w,h),flags=cv2.INTER_LINEAR)[:,:,None]*(1-weight)
   frame=np.clip(frame*(1-m)+refwarp*m,0,255).astype(np.uint8)
   transforms.append({'frame':i,'matrix':transform.tolist(),'speech_weight':float(weight)})
  encoder.stdin.write(frame.tobytes())
 encoder.stdin.close();assert encoder.wait()==0
 report={'segment':name,'source':str(source),'frames':len(frames),'fps':24,'dan_windows_local':windows,'reference_frame':reference_index,'reference_openness':openness(reference,refbox),'neutral_frames':int(np.count_nonzero(weights==0)),'transition_frames':int(np.count_nonzero((weights>0)&(weights<1))),'closure_tail_seconds':.1,'method':'Tracked neutral mouth patch outside saved Dan speech windows. Upper-face LK feature alignment preserves head movement; eyes, brows, body and background remain original. T04 speaking lips additionally re-driven from original d04+d05 audio.','affine_fallbacks':fallbacks,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'license':'Existing Wav2Lip performance terms: personal/noncommercial'}
 meta.write_text(json.dumps(report,indent=2)+'\n');np.save(target.with_suffix('.face-boxes.npy'),bounds);np.save(target.with_suffix('.speech-weights.npy'),weights);target.with_suffix('.tracking.json').write_text(json.dumps(transforms)+'\n')
 # Reference mouth and full neutral pose are retained for visual review.
 cv2.imwrite(str(OUT/'contacts'/f'{name}-neutral.jpg'),reference)
 reports.append(report);print('Corrected',name,'neutral frames',report['neutral_frames'],'reference',reference_index,flush=True)
reports=[json.loads((OUT/'mouths'/f'{n}.json').read_text()) for n in ['T04','T08','T10','T22','T26','T30'] if (OUT/'mouths'/f'{n}.json').exists()]
(OUT/'mouth-corrections.json').write_text(json.dumps(reports,indent=2)+'\n')
