#!/usr/bin/env python3
"""Make a measured original/new rehearsal comparison from a downloaded Runway result."""
from pathlib import Path
import argparse,json,subprocess,hashlib,re
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=ROOT/'build/first-trailer-visual-tests-v1/fielder-motion-test';OUT.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);args=p.parse_args();source=args.source.resolve();assert source.exists()
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)],text=True))
def ff(args):subprocess.run(['ffmpeg','-y','-v','error',*map(str,args)],check=True)
raw=probe(source);v=next(s for s in raw['streams'] if s['codec_type']=='video');duration=float(v.get('duration',raw['format']['duration']));assert duration>=7.9
font=Path.home()/'Library/Fonts/LiberationSans-Bold.ttf'
anchor=next((ROOT/'clips/v4').glob('*fielder-reaction-*.mp4'))
segments=[('original',anchor,'scale=1280:1920,crop=1280:720:0:467','ORIGINAL v10 REACTION / SOURCE 2-6s'),('new',source,'scale=1280:720','NEW REHEARSAL TEST 01 / SOURCE 2-6s')]
for name,path,vf,label in segments:
    vf+=f",drawbox=x=0:y=0:w=iw:h=42:color=black@0.9:t=fill,drawtext=fontfile={font}:text='{label}':fontsize=19:fontcolor=white:x=18:y=12"
    ff(['-ss',2,'-i',path,'-t',4,'-vf',vf,'-r',24,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',OUT/(name+'.mp4')])
(OUT/'concat.txt').write_text("file 'original.mp4'\nfile 'new.mp4'\n")
final=OUT/'fielder-original-versus-new-test-01.mp4';ff(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy','-movflags','+faststart',final])
viewing=OUT/'fielder-rehearsal-test-01.mp4'
ff(['-i',source,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',viewing])
view=probe(viewing);vv=next(s for s in view['streams'] if s['codec_type']=='video');assert int(vv['nb_read_frames'])==int(v['nb_read_frames'])
checks=[]
for name in ['original.mp4','new.mp4',final.name]:
    z=probe(OUT/name);stream=next(s for s in z['streams'] if s['codec_type']=='video');secs=8 if name==final.name else 4
    assert int(stream['nb_read_frames'])==secs*24 and abs(float(z['format']['duration'])-secs)<.001
    checks.append({'file':name,'duration':secs,'frames':secs*24,'minimum_picture_duration':2,'result':'PASS'})
thumbs=[]
for label,path,times in [('ORIGINAL',anchor,[2,4.3,4.75]),('NEW TEST',source,[0,2,3.5,4.8,6,7.8])]:
    for t in times:
        pathout=OUT/f'{label.split()[0].lower()}-{t:.2f}.jpg';vf='scale=1280:1920,crop=1280:720:0:467' if label=='ORIGINAL' else 'scale=1280:720';ff(['-ss',t,'-i',path,'-frames:v',1,'-vf',vf,pathout]);thumbs.append((f'{label} / {t:.2f}s',pathout))
sheet=Image.new('RGB',(1280,3*268),'#162025');d=ImageDraw.Draw(sheet);ft=ImageFont.truetype(str(font),17)
for i,(label,path) in enumerate(thumbs):
    x=i%3*426;y=i//3*268;im=Image.open(path);im.thumbnail((426,240));sheet.paste(im,(x,y));d.text((x+10,y+245),label,font=ft,fill='white')
sheet.save(OUT/'motion-contact-sheet.jpg')
report={'source':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_duration':duration,'native_frames':int(v['nb_read_frames']),'native_fps':v['r_frame_rate'],'native_dimensions':[v['width'],v['height']],'native_audio_streams':sum(s['codec_type']=='audio' for s in raw['streams']),'comparison_checks':checks,'status':'Technical comparison checks pass; gesture/identity/acting remain visual review.'};(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# Fielder motion test 01 — rendered review\n\nA separately generated silent rehearsal attempt, compared with the original v10 reaction. This test has not replaced the accepted D2-r1 trailer.\n\nNative generated clip: '+f"{duration:.3f}s, {v['nb_read_frames']} decoded frames, {v['width']}×{v['height']} at {v['r_frame_rate']} fps; {report['native_audio_streams']} audio streams.\n\n"+'## Explicit RULES.md duration audit\n\n| Comparison composition | Duration | Frames | Minimum | Result |\n|---|---:|---:|---:|---|\n| Original reaction source 2–6 | 4.000s | 96 | 2.000s | PASS |\n| New rehearsal source 2–6 | 4.000s | 96 | 2.000s | PASS |\n\nThe actual comparison export is 8.000 seconds / 192 frames at 1280×720 and 24fps. No other shot was shortened. Sources and original locked teaser dialogue/subtitles remain unchanged. No time stretching or artificial actor morphing was applied to the comparison.\n\nView motion-contact-sheet.jpg and play the actual result to assess face continuity, stable room and camera, visible reset, brow pinch, eye narrowing and dropped gaze. The contact sheet alone cannot establish fluid or convincing acting.\n';(OUT/'QC.md').write_text(md)
print(json.dumps(report,indent=2))
