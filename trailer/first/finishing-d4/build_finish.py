from pathlib import Path
import csv,json,subprocess,shutil,importlib.util
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');D3=ROOT/'build/first-trailer-picture-pass-d3';OUT=ROOT/'build/first-trailer-finishing-d4';HERE=ROOT/'trailer/first/finishing-d4'
ROWS=list(csv.DictReader((D3/'timeline.csv').open()));FONT=Path.home()/'Library/Fonts/LiberationSans-Bold.ttf'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'segments').mkdir(exist_ok=True)
SINGLE=['T02','T04','T07','T08','T09','T11','T12','T13','T15','T18','T22','T23','T25','T26','T27','T28','T30','T31','T35']
def ff(args):subprocess.run(['ffmpeg','-y','-v','error',*map(str,args)],check=True)
def picture():
 sources=[]
 for r in ROWS:
  n=r['segment'];ss=0;source=D3/'segments'/f'{n}.mp4'
  if n in SINGLE:source=OUT/'polished'/f'{n}.mp4'
  elif n=='T10':source=OUT/'polished/T10_dan.mp4'
  elif n in ['T39','T40']:source=OUT/'polished/T39_T40.mp4';ss=0 if n=='T39' else 5
  override=ROOT/'clips/first/finishing-d4/performance'/f'{n}.mp4'
  selected=override.with_suffix('.json')
  if override.exists() and selected.exists() and json.loads(selected.read_text()).get('selected_for_delivery'):source=override
  assert source.exists(),source
  target=OUT/'segments'/f'{n}.mp4'
  if not target.exists():
   if n in ['T37','T38']:shutil.copy2(source,target)
   else:
    label=f"drawbox=x=12:y=12:w=194:h=28:color=0x0a0e12:t=fill,drawtext=fontfile={FONT}:text='FINISH PASS D4':fontsize=16:fontcolor=white:x=22:y=18"
    if n=='T04' and source==override:
     label+=f",drawbox=x=36:y=475:w=274:h=94:color=black@0.55:t=fill,drawtext=fontfile={FONT}:text='DAN':fontsize=26:fontcolor=white:x=52:y=491,drawtext=fontfile={FONT.parent/'LiberationSans-Regular.ttf'}:text='CEO, Pinterest':fontsize=23:fontcolor=white:x=52:y=530"
    ff(['-ss',ss,'-i',source,'-t',r['duration_seconds'],'-vf','scale=1280:720,fps=24,'+label,'-an','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',target])
  sources.append({'segment':n,'source':str(source),'source_start':ss,'duration':float(r['duration_seconds'])})
 (OUT/'picture-sources.json').write_text(json.dumps(sources,indent=2)+'\n')
def score():
 p=ROOT/'trailer/first/build_animatic.py';spec=importlib.util.spec_from_file_location('score',p);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.OUT=OUT
 b.EVENTS.update(json.loads((OUT/'score/events.json').read_text())['events'])
 b.midi('ukulele');b.lily()
 p=OUT/'score/first_trailer_score.ly';s=p.read_text().replace('First trailer - animatic scratch score - 180 seconds','First trailer - finishing D4 - 180 seconds').replace('Original working arrangement','Original arrangement').replace('Plucked reference','Ukulele').replace('Plk.','Uke.')
 p.write_text(s);result=subprocess.run(['lilypond','-dno-point-and-click','-o',str(OUT/'score/first_trailer_score'),str(p)],capture_output=True,text=True,check=True);(OUT/'score/compile.log').write_text(result.stdout+result.stderr)
 print('Updated score and ukulele MIDI',flush=True)
def export():
 (OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in ROWS))
 ff(['-f','concat','-safe',0,'-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4'])
 style="FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=48"
 vf=f"subtitles={OUT/'captions.srt'}:fontsdir={FONT.parent}:force_style='{style}'"
 ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',vf,'-map','0:v','-map','1:a','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar',48000,'-t',180,'-movflags','+faststart',OUT/'first-trailer-finishing-d4.mp4'])
 print('Exported D4',flush=True)
if __name__=='__main__':
 import sys
 for name in sys.argv[1:] or ['picture','score','export']:globals()[name]()
