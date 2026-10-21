"""Audio-driven mouth replacement for the private YCSE finishing pass.
Model code/weights: official Rudrabha/Wav2Lip, personal/noncommercial use.
Only a softly feathered lower-face region is replaced; the original eyes,
expression, body, hands, room, and frame count remain in the original footage.
"""
from pathlib import Path
import sys,json,subprocess,hashlib,time,argparse
import cv2,numpy as np,torch,librosa
from scipy.signal import lfilter
from scipy.ndimage import median_filter
sys.path.insert(0,'/private/tmp/ycs-wav2lip')
from models import Wav2Lip
import face_detection
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser')
OUT=ROOT/'build/first-trailer-finishing-d4';D3=ROOT/'build/first-trailer-picture-pass-d3'
SR=16000;FPS=24
def load_audio(path,sr=SR):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar',str(sr),'-f','f32le','-'])
 return np.frombuffer(raw,'<f4').copy()
def mel(a):
 a=lfilter([1,-.97],[1],a)
 stft=librosa.stft(a,n_fft=800,hop_length=200,win_length=800)
 basis=librosa.filters.mel(sr=16000,n_fft=800,n_mels=80,fmin=55,fmax=7600)
 db=20*np.log10(np.maximum(1e-5,basis@np.abs(stft)))-20
 return np.clip(8*((db+100)/100)-4,-4,4)
def reader(path):
 v=cv2.VideoCapture(str(path));frames=[]
 while True:
  okay,f=v.read()
  if not okay:break
  frames.append(f)
 v.release();return frames
class Engine:
 def __init__(self):
  self.device='mps' if torch.backends.mps.is_available() else 'cpu'
  self.model=Wav2Lip();checkpoint=torch.jit.load('/private/tmp/ycs-wav2lip/checkpoints/wav2lip_gan.pth',map_location='cpu')
  self.model.load_state_dict(checkpoint.state_dict());del checkpoint
  self.model.eval().to(self.device)
  self.detector=face_detection.FaceAlignment(face_detection.LandmarksType._2D,device=self.device,flip_input=False)
  print('Engine ready:',self.device,flush=True)
 def boxes(self,frames,roi):
  x0,y0,xend,yend=roi;scale=384/(xend-x0)
  indices=list(range(0,len(frames),3))
  small=[cv2.resize(frames[i][y0:yend,x0:xend],(384,round((yend-y0)*scale))) for i in indices]
  detected=[]
  for i in range(0,len(small),4):detected+=self.detector.get_detections_for_batch(np.array(small[i:i+4]))
  valid=[(i,d) for i,d in zip(indices,detected) if d is not None]
  if not valid:raise RuntimeError('No face detected in ROI '+str(roi))
  xs=np.array([i for i,d in valid]);values=np.array([d for i,d in valid],float)/scale
  allbox=np.stack([np.interp(np.arange(len(frames)),xs,values[:,j]) for j in range(4)],axis=1)
  allbox=median_filter(allbox,size=(5,1),mode='nearest')
  result=[]
  for x1,y1,x2,y2 in allbox:
   height=y2-y1;width=x2-x1
   # Match the training face crop, including chin but very little forehead.
   result.append([max(x0,round(x1+x0)),max(y0,round(y1+y0)),min(xend,round(x2+x0)),min(yend,round(y2+y0+height*.045))])
  return np.array(result,int),len(valid),len(indices)
 def render(self,source,audio,output,roi=None):
  start=time.monotonic();frames=reader(source);assert frames
  h,w=frames[0].shape[:2];roi=roi or [0,0,w,h]
  bounds,valid,tried=self.boxes(frames,roi);a=load_audio(audio);a=np.pad(a,(0,max(0,round(len(frames)/FPS*SR)+1600-len(a))))
  spec=mel(a);chunks=[]
  for i in range(len(frames)):
   j=round(i*80/FPS);m=spec[:,j:j+16]
   if m.shape[1]<16:m=np.pad(m,((0,0),(0,16-m.shape[1])),constant_values=-4)
   chunks.append(m)
  output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
  proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p',str(output)],stdin=subprocess.PIPE)
  for offset in range(0,len(frames),12):
   originals=frames[offset:offset+12];coords=bounds[offset:offset+12]
   crops=np.array([cv2.resize(f[y1:y2,x1:x2],(96,96)) for f,(x1,y1,x2,y2) in zip(originals,coords)])
   masked=crops.copy();masked[:,48:]=0
   face=np.concatenate([masked,crops],axis=3).transpose(0,3,1,2)/255
   inputs=torch.from_numpy(face.astype(np.float32)).to(self.device)
   ms=torch.from_numpy(np.array(chunks[offset:offset+len(originals)],np.float32)[:,None]).to(self.device)
   with torch.inference_mode():pred=self.model(ms,inputs).cpu().numpy().transpose(0,2,3,1)*255
   for p,f,(x1,y1,x2,y2) in zip(pred,originals,coords):
    rh,rw=y2-y1,x2-x1;patch=cv2.resize(p,(rw,rh),interpolation=cv2.INTER_CUBIC)
    yy,xx=np.mgrid[:rh,:rw];u=(xx/(rw-1)-.5)/.44;v=(yy/(rh-1)-.77)/.30
    radius=np.sqrt(u*u+v*v);mask=np.clip((1-radius)/.22,0,1)
    # Keep nose/eyes original and make the transition into cheeks invisible.
    mask*=np.clip((yy/(rh-1)-.48)/.12,0,1);mask=mask[:,:,None]
    base=f[y1:y2,x1:x2].astype(float)
    f[y1:y2,x1:x2]=np.clip(base*(1-mask)+patch*mask,0,255).astype(np.uint8)
    proc.stdin.write(f.tobytes())
   if offset%120==0:print(output.stem,offset,'/',len(frames),flush=True)
  proc.stdin.close();assert proc.wait()==0
  report={'source':str(source),'audio':str(audio),'output':str(output),'frames':len(frames),'fps':24,'device':self.device,'roi':roi,'detected_face_samples':valid,'attempted_face_samples':tried,'box_min':bounds.min(axis=0).tolist(),'box_max':bounds.max(axis=0).tolist(),'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),'audio_sha256':hashlib.sha256(Path(audio).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,2),'method':'Wav2Lip GAN; feathered lower-face composite; original upper face and body retained','license':'personal/noncommercial only'}
  output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print('Complete',output.stem,report['seconds'],'seconds',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('audio');p.add_argument('output');p.add_argument('--roi',nargs=4,type=int);args=p.parse_args()
 Engine().render(Path(args.source),Path(args.audio),Path(args.output),args.roi)
