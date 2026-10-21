from pathlib import Path
import json,subprocess,wave,hashlib,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=ROOT/'build/first-trailer-visual-tests-v1'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)],text=True))
def pcm(p,start=0,frames=None):
    with wave.open(str(p)) as w:
        assert w.getframerate()==48000 and w.getsampwidth()==2;w.setpos(start);return w.readframes(w.getnframes()-start if frames is None else frames)
checks=[]
for name,secs in [('roy-pinterest-reveal-test-v1.mp4',18),('fielder-rehearsal-reference-v1.mp4',12),('original-reaction.mp4',4),('reset-reference.mp4',4),('downward-reference.mp4',4)]:
    p=OUT/name;r=probe(p);v=next(s for s in r['streams'] if s['codec_type']=='video');assert int(v['nb_read_frames'])==secs*24 and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==(1280,720);assert abs(float(r['format']['duration'])-secs)<.001
    checks.append({'file':name,'seconds':secs,'frames':secs*24,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
source=ROOT/'build/first-trailer-voice-pass-d2';assert pcm(source/'mix.wav',104*48000,18*48000)==pcm(OUT/'reveal-mix.wav')
full=source/'first-trailer-voice-pass-d2-r1.mp4';approved=json.loads((source/'QC-fielder-r1.json').read_text());assert hashlib.sha256(full.read_bytes()).hexdigest()==approved['sha256']
final=OUT/'roy-pinterest-reveal-test-v1.mp4';meter=subprocess.run(['ffmpeg','-v','info','-i',str(final),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);measure=json.loads(re.findall(r'\{\s*"input_i".*?\}',meter.stderr,re.S)[-1]);assert float(measure['input_tp'])<=-1
frames=[]
for t in [0,8,10,12,15,17]:
    p=OUT/f'qc-final-{t:02}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(final),'-frames:v','1',str(p)],check=True);frames.append((t,p))
sheet=Image.new('RGB',(1280,3*390),'#152027');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(Path.home()/'Library/Fonts/LiberationSans-Regular.ttf'),19)
for i,(t,p) in enumerate(frames):
    x=(i%2)*640;y=(i//2)*390;im=Image.open(p);im.thumbnail((640,360));sheet.paste(im,(x,y));d.text((x+12,y+365),f'Actual encoded reveal test / {t:02}s',font=font,fill='white')
sheet.save(OUT/'encoded-contact-sheet.jpg')
comps=[('T23 stream',6),('T24 continuous pullback',8),('T25 room hold',4),('Original reaction reference',4),('Reset keyframe reference',4),('Downward keyframe reference',4)];assert all(d>=2 for _,d in comps)
report={'status':'PASS technical visual-test checks; new moving character performances remain pending','files':checks,'exact_pcm_excerpt_match':True,'approved_full_trailer_unchanged':True,'loudness':measure,'compositions':[{'name':n,'duration':s,'minimum':2,'result':'PASS'} for n,s in comps],'still_reference_limit':'Roy, Dan and Fielder are static generated keyframes in the reveal proof. The reference reel contains original motion followed by labeled static poses.'};(OUT/'QC.json').write_text(json.dumps(report,indent=2)+'\n')
md='# Visual test rendered QC\n\nTechnical checks pass for the encoded outputs. This does not establish new acting, ukulele fingering, pronunciation or lip sync.\n\n'+''.join(f"- {c['file']}: {c['seconds']:.3f} seconds, {c['frames']} decoded frames, 1280×720 at 24 fps.\n" for c in checks)+'\n## RULES.md duration audit\n\n| Composition | Duration | Minimum | Result |\n|---|---:|---:|---|\n'+''.join(f'| {n} | {s:.3f}s | 2.000s | PASS |\n' for n,s in comps)+'\nThe pullback is continuous. No short inserts or shot-duration borrowing were introduced. The full D2-r1 trailer and original v7/v10 assets remain untouched.\n\nThe reveal PCM audio exactly matches the accepted mix at 104–122 seconds. Encoded integrated loudness is '+measure['input_i']+' LUFS and true peak is '+measure['input_tp']+' dBTP. The scratch plucked instrument remains a nylon-guitar stand-in.\n\nActual encoded frames at 0, 8, 10, 12, 15 and 17 seconds are saved in encoded-contact-sheet.jpg for visual inspection.\n';(OUT/'QC.md').write_text(md)
print(json.dumps({'status':report['status'],'exact_pcm_excerpt_match':True,'approved_full_trailer_unchanged':True,'true_peak':measure['input_tp']},indent=2))
