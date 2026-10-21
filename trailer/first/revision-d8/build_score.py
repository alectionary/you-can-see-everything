"""Write the 197-second score; sounding MIDI retains frame-based Roy attacks."""
from pathlib import Path
import importlib.util
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser');HERE=ROOT/'trailer/first/revision-d8';OUT=ROOT/'build/first-trailer-revision-d8'
def quantize_staff(es):
 by={round(e['t']*4)/4:dict(e,t=round(e['t']*4)/4) for e in es};keys=sorted(by);result=[]
 for i,t in enumerate(keys):
  e=by[t];end=min(t+.5,keys[i+1] if i+1<len(keys) else 197,197);e['d']=max(.25,end-t);result.append(e)
 return result
code=(ROOT/'trailer/first/revision-d6/build_revision.py').read_text()
code=code.replace("'191*480'","'197*480'").replace("'range(48)'","'range(50)'").replace("'a=bar*4;b=min(a+4,191)'","'a=bar*4;b=min(a+4,197)'")
code=code.replace('t==190','t==196')
code=code.replace('188*480','196*480').replace('variable(3*480)','variable(1*480)').replace('ff580403021808','ff580401021808').replace('if t==188','if t==196').replace("glob+='\\\\time 3/4 '","glob+='\\\\time 1/4 '")
code=code.replace('[32,64,96,128,160]','[32,64,96,128,160,192]')
a=code.index(' cues={',code.index('def score():'));z=code.index('\n for t in range(DURATION):',a)
cues={0:'Roy / hand-led strokes',12:'TRUTH / Roy stops',18:'Original simultaneous take',26:'Take 2 / same Dan',30:'Take 3 / same Dan',38:'Private messages',44:'CHARACTER HE CREATED',71:'CORPORATE COMMUNICATIONS',80:'PARKING',82:'Actual lot',85:'Friendly permit plan',100:'TROLLING',104:'Dan post / angry reactions',112:'Roy introduces / hand resting',118:'Roy starts playing',126:'DM / Nathan blocked',140:'Nathan post / I did not know',168:'Private DM to billboard',174:'BEYOND TRUTH',177:'Silence',179:'Single title attack',183:'Roy / room performance',193:'New Pinterest handle'}
code=code[:a]+' cues='+repr(cues)+code[z:]
code=code.replace('D6 - ukulele score / editorial revision','D8 - hand-led ukulele / editorial score').replace('3:11 | quarter','3:17 | quarter').replace('final bar is 3/4','final bar is 1/4')
code=code.replace('Roy retains natural microtiming. Low notes, sustains and distortion are studio transformations.','Roy staff rounds to 1/4 second; MIDI and audio retain measured frame timing. Low parts are studio transformations.')
code=code.replace('Cards add eleven seconds. Silence 2:51-2:53; title attack 2:53; no music after 2:57.','D8 adds six seconds. Silence 2:57-2:59; title 2:59; score ends 3:03; Roy plays to 3:13.')
code=code.replace("ns['notation'](es,role=='body')","ns['notation'](quantize_staff(es) if role=='roy' else es,role=='body')")
code=code.replace('ukulele-score-d6','ukulele-score-d8')
ns={'quantize_staff':quantize_staff};exec(compile(code,str(HERE/'score-adapter.py'),'exec'),ns);ns.update(OUT=OUT,HERE=HERE,DURATION=197);ns['score']()
