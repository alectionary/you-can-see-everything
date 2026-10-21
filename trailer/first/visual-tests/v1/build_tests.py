#!/usr/bin/env python3
"""Render a screen-compositing proof from generated keyframes; no character animation."""
from pathlib import Path
import json, subprocess, hashlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/'build/first-trailer-visual-tests-v1'
OUT.mkdir(parents=True,exist_ok=True)
FONTDIR=Path.home()/'Library/Fonts'
def font(n,bold=False):return ImageFont.truetype(str(FONTDIR/('LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf')),n)
def homography(src,dst):
    rows=[];values=[]
    for (x,y),(u,v) in zip(src,dst):
        rows.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);values.extend([u,v])
    h=np.append(np.linalg.solve(np.array(rows,float),np.array(values,float)),1).reshape(3,3)
    return h

def project(h,points):
    p=np.column_stack([points,np.ones(len(points))])@h.T
    return p[:,:2]/p[:,2:]
def warp(image,size,src,dst):
    # Pillow maps output coordinates back into input coordinates.
    h=homography(dst,src).reshape(-1)
    return image.transform(size,Image.Transform.PERSPECTIVE,tuple(h[:8]),Image.Resampling.BICUBIC,fillcolor=(0,0,0,0) if image.mode=='RGBA' else (0,0,0))

roy=Image.open(HERE/'roy-stream-master-v1.png').convert('RGB')
room=Image.open(HERE/'dan-fielder-monitor-clean-v1.png').convert('RGB')
page=Image.new('RGB',(1920,1080),'#ffffff');d=ImageDraw.Draw(page)
d.line((0,120,1920,120),fill='#e7e7e7',width=2)
d.ellipse((46,34,100,88),fill='#e60023');d.text((62,38),'P',font=font(40,True),fill='white')
d.text((116,42),'Pinterest',font=font(37,True),fill='#242424')
d.text((340,48),'Home',font=font(26,True),fill='#252525');d.text((460,48),'Explore',font=font(26),fill='#555555')
d.rounded_rectangle((615,28,1710,94),radius=33,fill='#eeeeee');d.text((650,47),'Search',font=font(27),fill='#777777')
d.ellipse((1795,34,1850,89),fill='#e7e7e7');d.text((1810,44),'D',font=font(28,True),fill='#555555')
d.text((130,163),'ROY FINDS HIS VOICE',font=font(49,True),fill='#222222')
d.text((132,222),'Roy  /  Live music',font=font(25),fill='#626262')
video=np.array([[130,278],[1310,278],[1310,942],[130,942]],float)
page.paste(roy.resize((1180,664),Image.Resampling.LANCZOS),(130,278))
d.rounded_rectangle((1350,165,1545,228),radius=31,fill='#e60023');d.text((1410,182),'Save',font=font(29,True),fill='white')
d.text((1350,280),'Original stream',font=font(29,True),fill='#222222')
d.text((1350,334),'Watch on Pinterest',font=font(25),fill='#555555')
d.line((1350,395,1815,395),fill='#e5e5e5',width=2)
d.text((1350,439),'Comments',font=font(29,True),fill='#222222')
d.rounded_rectangle((1350,505,1810,576),radius=30,fill='#eeeeee');d.text((1380,526),'Add a comment',font=font(24),fill='#777777')
d.text((132,974),'Live from Roy\u2019s room',font=font(27),fill='#444444')
page.save(HERE/'pinterest-wrapper-v1.png')
# Measured inner-display corners on the generated 1672x941 plate, clockwise TL/TR/BR/BL.
screen=np.array([[51,178],[820,194],[823,608],[42,671]],float)
pagecorners=np.array([[0,0],[1920,0],[1920,1080],[0,1080]],float)
roomcorners=np.array([[0,0],[room.width,0],[room.width,room.height],[0,room.height]],float)
h=homography(pagecorners,screen);royquad=project(h,video)
page_warp=warp(page.convert('RGBA'),room.size,pagecorners,screen)
scene=Image.alpha_composite(room.convert('RGBA'),page_warp).convert('RGB')
W,H,FPS=1280,720,24
outputcorners=np.array([[0,0],[W,0],[W,H],[0,H]],float)

def ease(u):return u*u*(3-2*u)
def camera(t):
    if t<6:return royquad
    if t<10:
        u=ease((t-6)/4);return royquad*(1-u)+screen*u
    if t<14:
        u=ease((t-10)/4);return screen*(1-u)+roomcorners*u
    return roomcorners

def label(frame):
    d=ImageDraw.Draw(frame);d.rectangle((0,H-40,W,H),fill='#10191d')
    d.text((18,H-30),'SCREEN COMPOSITING TEST  /  STILL REFERENCES  /  TEMP UKULELE',font=font(17,True),fill='#dce5e7')
    return frame

raw=OUT/'reveal-picture.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',str(raw)],stdin=subprocess.PIPE)
for i in range(18*FPS):
    view=camera(i/FPS);view_h=homography(view,outputcorners)
    frame=warp(room,(W,H),view,outputcorners).convert('RGBA')
    # Render each layer directly at output resolution; do not magnify a baked monitor image.
    ui=warp(page.convert('RGBA'),(W,H),pagecorners,project(view_h,screen))
    live=warp(roy.convert('RGBA'),(W,H),np.array([[0,0],[roy.width,0],[roy.width,roy.height],[0,roy.height]],float),project(view_h,royquad))
    frame=label(Image.alpha_composite(Image.alpha_composite(frame,ui),live).convert('RGB'))
    proc.stdin.write(frame.tobytes())
    if i in [0,6*FPS,10*FPS,14*FPS,17*FPS]:frame.save(OUT/f'reveal-{i//FPS:02}.jpg')
proc.stdin.close();assert proc.wait()==0
src=ROOT/'build/first-trailer-voice-pass-d2';srt='1\n00:00:00,800 --> 00:00:05,000\nThis next one\u2019s about someone I used to work with.\n\n2\n00:00:14,400 --> 00:00:16,600\nDid you arrange this?\n'
(OUT/'reveal-captions.srt').write_text(srt)
# Keep this compositing proof on the accepted D2-r1 sound timeline, sample-for-sample.
subprocess.run(['ffmpeg','-y','-v','error','-ss','104','-i',str(src/'mix.wav'),'-t','18','-c:a','pcm_s16le',str(OUT/'reveal-mix.wav')],check=True)
final=OUT/'roy-pinterest-reveal-test-v1.mp4'
style="FontName=Liberation Sans,FontSize=21,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,Outline=2,Shadow=0,Alignment=2,MarginV=58"
subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-i',str(OUT/'reveal-mix.wav'),'-vf',f"subtitles={OUT/'reveal-captions.srt'}:fontsdir={FONTDIR}:force_style='{style}'",'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-t','18','-movflags','+faststart',str(final)],check=True)
# Original motion anchor and generated static pose references; no simulated actor animation.
source=next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4'))
ff=['ffmpeg','-y','-v','error']
parts=[('original-reaction',source,True,4),('reset-reference',HERE/'fielder-reset-v1.png',False,4),('downward-reference',HERE/'fielder-downward-glance-v1.png',False,4)]
labels=['ORIGINAL REACTION  /  SOURCE 2-6s  /  v10 ~39s ANCHOR','REHEARSAL RESET  /  GENERATED STATIC REFERENCE','SQUINT + DOWNWARD GLANCE  /  GENERATED STATIC REFERENCE']
for (name,p,moving,duration),text in zip(parts,labels):
    args=ff+(['-ss','2','-i',str(p)] if moving else ['-loop','1','-framerate','24','-i',str(p)])
    vf=('scale=1280:1920,crop=1280:720:0:467' if moving else 'scale=1280:720')+f",drawbox=x=0:y=0:w=iw:h=42:color=black@0.9:t=fill,drawtext=fontfile={FONTDIR/'LiberationSans-Bold.ttf'}:text='{text}':fontsize=18:fontcolor=white:x=18:y=12"
    subprocess.run(args+['-t',str(duration),'-vf',vf,'-r','24','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],check=True)
(OUT/'reaction-concat.txt').write_text(''.join(f"file '{name}.mp4'\n" for name,_,_,_ in parts))
subprocess.run(ff+['-f','concat','-safe','0','-i',str(OUT/'reaction-concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'fielder-rehearsal-reference-v1.mp4')],check=True)
composition={'method':'Still-keyframe camera and screen composite; no new moving character footage','fps':24,'segments':[{'id':'T23','start':0,'end':6,'duration':6},{'id':'T24','start':6,'end':14,'duration':8},{'id':'T25','start':14,'end':18,'duration':4}],'screen_corners':screen.tolist(),'stream_viewport_page':video.tolist(),'source_audio_start':104,'source_audio_end':122,'same_stream_image_every_frame':str(HERE/'roy-stream-master-v1.png'),'source_audio_sha256':hashlib.sha256((src/'mix.wav').read_bytes()).hexdigest(),'output':str(final)}
(OUT/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
print('Rendered reveal proof and rehearsal reference reel:',OUT)
