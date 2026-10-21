from pathlib import Path
import cv2,numpy as np,json
from scipy.signal import find_peaks,savgol_filter
from PIL import Image,ImageDraw
R=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');O=R/'build/first-trailer-revision-d8'
jobs=[('opening',R/'clips/first/picture-pass-d3/roy-stream.mp4',0,8,0),('apology',R/'clips/first/picture-pass-d3/roy_end.mp4',2,4,8),('middle',R/'clips/first/picture-pass-d3/roy_continuous.mp4',0,14,112),('ending',R/'clips/first/picture-pass-d3/roy_end.mp4',0,10,181)]
out=[]
for name,path,ss,dur,start in jobs:
 c=cv2.VideoCapture(str(path));c.set(cv2.CAP_PROP_POS_MSEC,ss*1000);gray=None;values=[];signed=[];frames=[]
 for i in range(round(dur*24)):
  ok,z=c.read();assert ok
  g=cv2.cvtColor(z[510:680,425:630],cv2.COLOR_BGR2GRAY)
  if gray is None:values.append(0);signed.append(0)
  else:
   flow=cv2.calcOpticalFlowFarneback(gray,g,None,.5,3,19,3,5,1.2,0);mag=np.linalg.norm(flow,axis=2);mask=(mag>.35)&(mag<25);values.append(float(np.percentile(mag,70)));signed.append(float(np.median(flow[:,:,1][mask])) if np.any(mask) else 0)
  gray=g
  if i%12==0:frames.append(z[470:700,380:700])
 c.release();v=savgol_filter(values,5,2);peaks,_=find_peaks(v,distance=6,prominence=max(.2,float(np.percentile(v,90))*.13),height=max(.5,float(np.percentile(v,90))*.19));times=[round(float(i/24),6) for i in peaks]
 # First visible stroke is already underway in each source's initial pose.
 if not times or times[0]>.28:times.insert(0,0.)
 item={'key':name,'source':str(path),'source_start':ss,'duration':dur,'timeline_start':start,'roi':[425,510,630,680],'onsets_local':times,'onsets_global':[round(start+t,6) for t in times],'flow_energy':values,'signed_y_flow':signed};out.append(item)
 im=Image.new('RGB',(1280,80+180*((len(frames)+5)//6)),(20,20,20));d=ImageDraw.Draw(im);d.text((10,10),name+' visual hand motion; onsets '+str(times),fill='white')
 for j,f in enumerate(frames):
  im.paste(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((210,151)),((j%6)*213,60+(j//6)*180));d.text(((j%6)*213,212+(j//6)*180),str(j*.5),fill='white')
 im.save(O/'contacts'/f'{name}-hand-motion.jpg');print(name,times,flush=True)
(O/'hand-motion.json').write_text(json.dumps(out,indent=2)+'\n')
