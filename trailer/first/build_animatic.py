#!/usr/bin/env python3
"""Build the first trailer's labeled animatic, scratch score and review measurements.
Run with the bundled Python containing numpy and Pillow; requires ffmpeg, LilyPond,
FluidSynth, macOS say and the installed GeneralUser GS SoundFont. No paid APIs.
"""
from pathlib import Path
from fractions import Fraction
import argparse, csv, json, math, struct, subprocess, wave, hashlib, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'build/first-trailer-animatic'
LABEL='ANIMATIC D1'
AUDIO_LABEL='TEMP VOICES + SCRATCH MUSIC'
OUTPUT_NAME='first-trailer-animatic-d1.mp4'
W,H,FPS,SR=1280,720,24,48000
FONTDIR=Path.home()/'Library/Fonts'
FONTS={n:FONTDIR/f'LiberationSans-{n}.ttf' for n in ('Regular','Bold','Italic')}
BG=(18,23,28); FG=(237,234,226); MUTED=(168,178,181); ACCENT=(151,194,178)

def run(args,**kw):
    return subprocess.run([str(a) for a in args],check=True,**kw)
def ff(args,**kw): return run(['ffmpeg','-y','-v','error',*args],**kw)
def font(size,bold=False):return ImageFont.truetype(str(FONTS['Bold' if bold else 'Regular']),size)
def txt(im,xy,s,size=26,fill=FG,bold=False):ImageDraw.Draw(im).text(xy,s,font=font(size,bold),fill=fill)
def wrapped(im,s,xy,width=42,size=26,fill=FG):
    x,y=xy
    for line in textwrap.wrap(s,width):txt(im,(x,y),line,size,fill);y+=int(size*1.35)
    return y

def fit(path,size=(W,H),dark=1):
    im=ImageOps.fit(Image.open(path).convert('RGB'),size,centering=(.5,.38))
    return ImageEnhance.Brightness(im).enhance(dark)
def board(title,note,ref=None):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    if ref:
        im.paste(fit(ref,(670,610)),(0,48))
        d.rectangle((670,48,W,H),fill=BG)
    x=710 if ref else 70
    txt(im,(x,110),title,30,ACCENT,True)
    wrapped(im,note,(x,174),31 if ref else 68,26)
    txt(im,(x,530),'STORYBOARD PLACEHOLDER',18,MUTED,True)
    txt(im,(x,558),'New coverage has not been filmed.',17,MUTED)
    return im

def chrome(im,row,status):
    d=ImageDraw.Draw(im);d.rectangle((0,0,W,48),fill=(10,14,18))
    txt(im,(22,12),'YOU CAN SEE EVERYTHING  /  FIRST TRAILER',18,FG,True)
    txt(im,(775,12),f'{row["segment"]}  |  {status}',17,ACCENT)
    d.rectangle((0,672,W,H),fill=(10,14,18))
    txt(im,(22,686),LABEL+'  |  '+AUDIO_LABEL,16,MUTED)
    txt(im,(1010,686),f'{float(row["start_seconds"]):06.1f} - {float(row["end_seconds"]):06.1f}s',16,MUTED)
    return im

def document(kind):
    im=Image.new('RGB',(W,H),(222,225,221));d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,65,1210,650),18,fill=(249,248,243))
    d.ellipse((102,96,146,140),fill=(181,32,47));txt(im,(116,99),'P',30,(255,255,255),True)
    txt(im,(163,103),'PINTEREST',23,(45,49,49),True)
    if kind=='prep':
        txt(im,(112,184),'DOCUMENTARY PREPARATION',32,(35,42,42),True)
        txt(im,(112,228),'COMMUNICATIONS REVIEW',20,(91,103,98))
        txt(im,(112,307),'Distribution review',29,(45,49,49))
        txt(im,(112,350),'Primary destination: Pinterest',24,(91,103,98))
        for y,label in [(390,'Keep this in Dan’s own words.'),(475,'Can this feel less prepared?')]:
            d.rounded_rectangle((110,y,1160,y+64),10,fill=(230,238,230));txt(im,(132,y+18),label,27,(47,71,59))
    else:
        txt(im,(112,180),'DISTRIBUTION STRATEGY',32,(35,42,42),True)
        txt(im,(112,228),'Keep the conversation on Pinterest',24,(91,103,98))
        im.paste(fit(OUT/'plates/demolition.jpg',(650,310)),(112,290))
        wrapped(im,'Creative review\nPicture select: demolition',(810,330),21,25,(45,49,49))
    return im

def silhouette(label,question,uke=False):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.ellipse((230,130,420,320),fill=(75,85,88));d.rounded_rectangle((135,335,515,650),90,fill=(66,77,80))
    if uke:
        d.ellipse((290,390,440,560),fill=(174,130,74));d.ellipse((365,355,465,465),fill=(174,130,74));d.polygon([(395,420),(425,435),(580,210),(551,190)],fill=(140,105,65));d.ellipse((355,420,393,458),fill=(43,38,31))
    txt(im,(650,135),label,32,ACCENT,True)
    wrapped(im,question,(650,205),30,28)
    txt(im,(650,530),'CASTING STORYBOARD',18,MUTED,True)
    txt(im,(650,560),'No replacement actor has been cast.',17,MUTED)
    return im

def lodge(stage):
    im=Image.new('RGB',(W,H),(28,30,33));d=ImageDraw.Draw(im)
    for x in (65,370,675,980):
        d.rectangle((x,85,x+230,360),fill=(54,67,74));d.polygon([(x,295),(x+100,170),(x+210,295)],fill=(185,190,187))
    d.rectangle((0,490,W,H),fill=(51,44,40))
    d.rectangle((450,128,825,470),fill=(127,99,55));d.rectangle((467,145,808,451),fill=(177,155,119))
    d.polygon([(490,180),(640,160),(685,340),(510,405)],fill=(78,100,108));d.polygon([(625,182),(780,220),(735,410),(615,355)],fill=(170,95,75));d.ellipse((575,215,685,330),fill=(207,185,132))
    if stage=='shred':
        d.rectangle((448,388,830,450),fill=(15,17,18))
        for x in range(470,810,17):d.rectangle((x,445,x+9,585),fill=(177+(x%3)*8,145,110))
    if stage=='guests':
        for x in (130,300,930,1100):d.ellipse((x,350,x+65,415),fill=(100,107,110));d.rounded_rectangle((x-25,415,x+90,650),25,fill=(59,65,70))
    d.rectangle((0,575,W,672),fill=BG)
    txt(im,(38,590),{'event':'SKI LODGE / PICASSO EVENT','shred':'CONTINUOUS SHREDDING SHOT','guests':'GUESTS / PHONE RECORDING / TENTATIVE APPLAUSE'}[stage],27,ACCENT,True)
    txt(im,(38,632),'SCHEMATIC ONLY - NEW FOOTAGE REQUIRED',18,MUTED)
    return im

def stream():
    im=fit(HERE/'refs/ROY_v4.jpg')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((35,70,130,108),8,fill=(171,39,46));txt(im,(52,77),'LIVE',20,(255,255,255),True)
    txt(im,(150,77),'12 viewers',20)
    d.rounded_rectangle((780,110,1240,270),12,fill=(18,23,28));wrapped(im,'Roy’s ukulele stream\nPerformance placeholder',(805,135),29,25)
    txt(im,(36,575),'REFERENCE STILL / UKULELE PERFORMANCE TO CREATE',19,FG,True)
    return im

def wrapper_room():
    im=Image.new('RGB',(W,H),(29,33,36));d=ImageDraw.Draw(im)
    # Full scene is an editorial storyboard, not a generated new room.
    d.rounded_rectangle((64,74,1055,650),14,fill=(69,75,77))
    d.rounded_rectangle((80,90,1040,630),10,fill=(244,243,236))
    d.ellipse((100,110,133,143),fill=(180,32,46));txt(im,(109,110),'P',24,(255,255,255),True)
    txt(im,(151,115),'PINTEREST',20,(40,44,42),True)
    txt(im,(150,153),'ROY FINDS HIS VOICE',26,(40,44,42),True)
    im.paste(stream().resize((784,441)),(150,195))
    im.paste(fit(HERE/'refs/DAN_v3.jpg',(190,335)),(1065,252))
    txt(im,(1065,602),'DAN',20,ACCENT,True)
    return im

def editor(review=False):
    im=Image.new('RGB',(W,H),(32,36,41));d=ImageDraw.Draw(im)
    txt(im,(55,78),'DOCUMENTARY / EDIT REVIEW',25,FG,True)
    im.paste(fit(HERE/'refs/FIELDER_reaction_39s.jpg',(640,360)),(55,125))
    d.rounded_rectangle((730,125,1220,485),12,fill=(53,60,66))
    txt(im,(755,150),'Communications review' if review else 'REACTION SELECTS',23,ACCENT,True)
    wrapped(im,'Use the earlier reaction.' if review else 'Take 1: source\nTake 2: to create\nTake 3: to create',(755,205),27,25)
    thumb=fit(HERE/'refs/FIELDER_reaction_39s.jpg',(185,104))
    for i,label in enumerate(['SOURCE','PLACEHOLDER 2','PLACEHOLDER 3','SOURCE']):
        x=55+i*230;im.paste(thumb,(x,515));txt(im,(x,627),label,15,MUTED)
    return im

TITLES={
'T01':('ROY / STREAM SETUP','A private recovery ritual. A missed chord, then another attempt.'),
'T02':('ROY / START AGAIN','An apology, without a comic reaction.'),'T03':('ROY / IT HELPED','A separate interview question plays over the restarted performance.'),
'T06':('FIELDER / TAKE TWO','Practice the brow pinch, squint, and downward glance from v10 at 39 seconds.'),'T07':('FIELDER / TAKE THREE','Repeat the squint and dropped gaze, then question the previous attempt.'),'T09':('FIELDER / I WAS','The performance of confusion does not resolve his actual confusion.'),
'T08':('DAN / REHEARSAL NOTE','Mildly helpful: I thought you looked confused.'),'T22':('DAN / WHY THIS FILM','Pinterest’s CEO wants the conversation to happen on his platform.'),'T26':('DAN / ROY CHOSE THE SONG','A precise answer that leaves the arrangement unresolved.'),'T30':('DAN / IN THE SONG?','He calmly narrows the meaning of involved.'),
'T15':('CORPORATE COMMUNICATIONS','A staff member sits just beyond the interview frame.'),'T18':('WHICH VERSION?','A routine question inside an increasingly compromised review process.'),
'T25':('WATCHING ROY','Fielder asks whether Dan arranged the stream. Same viewing position as the pullback.'),'T31':('ROY / SOMETHING OFFSCREEN','He looks beyond the streaming camera. We do not reveal what he sees.'),'T36':('REAL ROY / WATCHING','He watches a monitor. His interrupted statement comes from the stream.')}

def make_plates(rows):
    for r in rows:
        n=r['segment'];p=OUT/'plates'/f'{n}.png'
        if n in ('T04','T05','T16','T17','T32'):continue
        if n=='T37':im=Image.new('RGB',(W,H),'black')
        elif n=='T38':
            im=Image.new('RGB',(W,H),'black');s='YOU CAN SEE EVERYTHING';bb=ImageDraw.Draw(im).textbbox((0,0),s,font=font(43));txt(im,((W-(bb[2]-bb[0]))//2,333),s,43)
        elif n=='T14':im=document('prep')
        elif n=='T33':im=document('campaign')
        elif n in ('T28','T34'):im=editor()
        elif n=='T29':im=editor(True)
        elif n in ('T11','T12','T13','T35'):im=silhouette({'T11':'ROY CANDIDATE A','T12':'ROY CANDIDATE B','T13':'ROY CANDIDATE C','T35':'REPLACEMENT ROY'}[n],'What does a rehearsed assurance look like?')
        elif n=='T27':im=silhouette('ROY CANDIDATE A','The same candidate returns with a ukulele.',True)
        elif n in ('T19','T20','T21'):im=lodge({'T19':'event','T20':'shred','T21':'guests'}[n])
        elif n in ('T23','T39','T40'):
            im=stream()
            if n=='T40':
                d=ImageDraw.Draw(im);d.rounded_rectangle((55,427,790,527),16,fill=(245,243,235));txt(im,(80,443),'PINTEREST',21,(176,31,44),True);txt(im,(80,476),'We hear you, Roy.',28,(37,44,40))
        elif n=='T24':im=wrapper_room()
        elif n=='T10':
            im=board('ROY DECLINES','One continuous table two-shot: refusal, pause, practical substitution.');im.paste(fit(HERE/'refs/FIELDER_v4.jpg',(370,380)),(60,230));im.paste(fit(HERE/'refs/DAN_v3.jpg',(370,380)),(450,230));txt(im,(860,300),'TABLE TWO-SHOT',22,ACCENT,True);wrapped(im,'New scene to create',(860,350),18,25)
        else:
            title,note=TITLES[n];ref=None
            if n.startswith('T') and n in ('T01','T02','T03','T31','T36'):ref=HERE/'refs/ROY_v4.jpg'
            elif n in ('T06','T07','T09'):ref=HERE/'refs/FIELDER_v4.jpg'
            elif n in ('T08','T22','T26','T30','T25'):ref=HERE/'refs/DAN_v3.jpg'
            im=board(title,note,ref)
        if n not in ('T37','T38'):chrome(im,r,'STORYBOARD' if n!='T14' and n!='T33' else 'SCREEN MOCKUP')
        im.save(p)

# Quarter-note clock, one tick = 1/4 quarter = 0.25 seconds.
INSTR={'ukulele':24,'piano':0,'bass':38,'strings':48,'brass':57,'percussion':115}
EVENTS={k:[] for k in INSTR}
def event(staff,t,d,notes,v):
    if t<164 and t+d>164:d=164-t
    EVENTS[staff].append(dict(t=float(t),d=float(d),notes=list(notes),v=int(v)))
def compose():
    phrase=[57,64,60,64]
    for start in (1,12,16,104,108,112,116,120):
        for j,n in enumerate(phrase):
            if start==1 and j==2:n=61
            if start==1 and j==3:continue
            if start<18 and start+j>=18:continue
            event('ukulele',start+j,.5 if start<8 else .75,[n],56 if start<18 else 64)
    for start in (18,26,34,42,50,58,66,74,82,94,106,114,122,130,138,146):
        for j,n in enumerate(phrase[:3]):
            notes=[n]
            if start>=40 and j==2:notes=[n,n+1]
            if start>=62 and j==0:notes=[n-6,n,n+1]
            event('piano',start+j*1.5,.5,notes,min(91,43+int(start*.27)))
    for t in np.arange(150,164,.5):event('piano',t,.25,[57+(int(t*2)%4),58+(int(t*2)%4),66],89)
    for t in range(40,164):
        step=4 if t<62 else 2 if t<104 else 1
        if t%step:continue
        note=33 if t<82 else [33,28,34,33][(t//4)%4]
        if 109<=t<126:continue
        event('bass',t,.75 if t<126 else .5,[note],min(112,42+int((t-40)*.65)))
    for t in np.arange(109.5,125.5,1):event('bass',t,.75,[33,28,34,33][int(t-109.5)%4:int(t-109.5)%4+1],84)
    for t in np.arange(126,164,.5):
        if float(t).is_integer():continue
        event('bass',t,.25,[33 if int(t)%4 else 34],85)
    for t in range(62,164,4):
        chord=[57,60,64] if t<82 else [57,58,64] if t<126 else [57,58,63,64] if t<148 else [57,58,59,64,66]
        event('strings',t,min(4,164-t),chord,min(110,35+int((t-62)*.72)))
    for t in range(148,164,2):event('brass',t,1.5,[33,39,46],90+(t-148))
    for t in np.arange(90,164,.5 if True else 1):
        if t<126 and int(t*2)%3:continue
        event('percussion',t,.25,[36],45 if t<126 else 67 if t<148 else 82)
    for k,ns in [('piano',[33,45,57,58,59,60,63,64,66]),('bass',[33]),('strings',[57,58,63,64,65,66]),('brass',[33,39,46])]:event(k,166,4,ns,118)
    for key in EVENTS:
        EVENTS[key].sort(key=lambda e:e['t'])
        last=0
        for e in EVENTS[key]:
            assert e['t']>=last,(key,e,last)
            last=e['t']+e['d']
        assert last<=180
    (OUT/'score/events.json').write_text(json.dumps({'tempo_quarter':60,'duration_seconds':180,'instruments':INSTR,'events':EVENTS},indent=2))

def vlq(n):
    out=[n&127];n>>=7
    while n:out.insert(0,(n&127)|128);n>>=7
    return bytes(out)
def midi(staff):
    ev=[(0,0,b'\xff\x51\x03\x0f\x42\x40'),(0,1,bytes([0xc0,INSTR[staff]]))]
    for e in EVENTS[staff]:
        for n in e['notes']:
            ev.append((round(e['t']*480),2,bytes([0x90,n,e['v']])))
            ev.append((round((e['t']+e['d'])*480),0,bytes([0x80,n,0])))
    data=b'';last=0
    for tick,priority,msg in sorted(ev,key=lambda x:(x[0],x[1])):data+=vlq(tick-last)+msg;last=tick
    data+=vlq(180*480-last)+b'\xff\x2f\x00'
    (OUT/'score'/f'{staff}.mid').write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',len(data))+data)
def pitch(n):
    names=['c','cis','d','ees','e','f','fis','g','aes','a','bes','b'];octave=n//12-4
    return names[n%12]+("'"*octave if octave>=0 else ','*(-octave))
def notation(staff):
    events=EVENTS[staff];pieces=[]
    for bar in range(45):
        a,b=bar*4,(bar+1)*4
        relevant=[e for e in events if e['t']<b and e['t']+e['d']>a]
        points=sorted({a,b,*[max(a,e['t']) for e in relevant],*[min(b,e['t']+e['d']) for e in relevant]})
        for lo,hi in zip(points,points[1:]):
            e=next((e for e in relevant if e['t']<=lo<e['t']+e['d']),None)
            ticks=round((hi-lo)*4);cursor=lo
            while ticks:
                length=next(v for v in (16,8,4,2,1) if v<=ticks)
                dur={16:'1',8:'2',4:'4',2:'8',1:'16'}[length]
                note='r' if e is None else '<'+' '.join(pitch(n) for n in e['notes'])+'>'
                dyn='' if e is None or cursor!=e['t'] else ('\\pp' if e['v']<50 else '\\p' if e['v']<70 else '\\mf' if e['v']<90 else '\\f' if e['v']<110 else '\\fff')
                tie='~' if e and cursor+length/4<e['t']+e['d'] else ''
                pieces.append(note+dur+dyn+tie);ticks-=length;cursor+=length/4
        pieces.append('|\n')
    return ' '.join(pieces)
def lily():
    cues={0:'0:00 Roy alone',18:'0:18 Rehearsal',40:'0:40 Casting',62:'1:02 Corporate review',82:'1:22 Publicity',104:'1:44 The stream',126:'2:06 Authenticity',148:'2:28 Fracture',164:'2:44 Silence',166:'2:46 Title',170:'2:50 Roy returns'}
    glob='\\numericTimeSignature \\time 4/4 \\tempo 4 = 60 \\key a \\minor\n'
    for t in range(180):
        if t in cues:glob+='\\mark \\markup \\small "'+cues[t]+'" '
        glob+='s4 '+('|\n' if (t+1)%4==0 else '')
        if t+1 in (32,64,128,160):glob+='\\break '
        if t+1==96:glob+='\\pageBreak '
    s='\\version "2.24.3"\n#(set-global-staff-size 18)\n\\header { title = "YOU CAN SEE EVERYTHING" subtitle = "First trailer - animatic scratch score - 180 seconds" composer = "Original working arrangement" tagline = ##f }\n'
    s+='global = { '+glob+' }\n'
    for staff in EVENTS:s+=staff+'Music = \\absolute { '+notation(staff)+' }\n'
    s+='\\paper { #(set-paper-size "a3" ) indent = 24\\mm short-indent = 12\\mm }\n\\score { <<\n'
    names={'ukulele':('Plucked reference','Plk.','acoustic guitar (nylon)','treble'),'piano':('Piano','Pno.','acoustic grand','treble'),'bass':('Bass pulse','Bass','synth bass 1','bass'),'strings':('Strings','Str.','string ensemble 1','treble'),'brass':('Brass','Br.','trombone','bass'),'percussion':('Mechanism rhythm','Rhy.','woodblock','bass')}
    for staff,(name,short,inst,clef) in names.items():s+=f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}" midiInstrument = "{inst}" }} << \\global {{ \\clef {clef} \\{staff}Music }} >>\n'
    s+='>> \\layout { } \\midi { \\tempo 4 = 60 } }\n'
    (OUT/'score/first_trailer_score.ly').write_text(s)
    result=run(['lilypond','-o',OUT/'score/first_trailer_score',OUT/'score/first_trailer_score.ly'],capture_output=True,text=True)
    (OUT/'score/compile.log').write_text(result.stdout+result.stderr)

def load_audio(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ac','1','-ar',str(SR),'-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4').copy()
def write_wav(path,a):
    a=np.asarray(a,dtype=np.float32);samples=np.rint(np.clip(a,-1,1)*32767).astype('<i2')
    with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(samples.tobytes())
def add(dest,a,t,gain=1):
    start=round(t*SR);end=min(len(dest),start+len(a));dest[start:end]+=a[:end-start]*gain

def speech(lines):
    dest=np.zeros(180*SR,np.float32);report=[];subs=[]
    voices={'DAN':'Reed (English (US))','FIELDER':'Daniel','ROY':'Eddy (English (US))','ROY CANDIDATE A':'Reed (English (US))','ROY CANDIDATE B':'Daniel','ROY CANDIDATE C':'Eddy (English (US))','COMMUNICATIONS':'Samantha','EDITOR':'Samantha','OFFSCREEN DIRECTOR':'Samantha','OFFSCREEN CREW':'Daniel'}
    for line in lines:
        padding={'head':5,'tail':10}
        lid=line['line_id'];start=float(line['start_seconds']);end=float(line['end_seconds']);path=OUT/'speech'/f'{lid}.aiff'
        if line['source'].startswith(('reuse ','file ')):
            source=ROOT/line['source'].split(' ',1)[1].split(';',1)[0];a=load_audio(source)
            if source.with_suffix('.json').exists():
                padding.update(json.loads(source.with_suffix('.json').read_text()).get('speech_trim_padding_ms',{}))
        else:
            metadata=path.with_suffix('.txt')
            identity=json.dumps([voices[line['speaker']],175,line['text']],ensure_ascii=False)
            if not path.exists() or not metadata.exists() or metadata.read_text()!=identity:
                run(['say','-v',voices[line['speaker']],'-r','175','-o',path,line['text']])
                metadata.write_text(identity)
            a=load_audio(path)
        peak=float(np.max(np.abs(a)))
        if peak<.0001:raise ValueError('Empty temporary speech: '+lid)
        active=np.flatnonzero(np.abs(a)>peak*.012)
        a=a[max(0,int(active[0])-round(padding['head']*SR/1000)):min(len(a),int(active[-1])+round(padding['tail']*SR/1000)+1)]
        actual=len(a)/SR
        # Natural synth timing is retained. Caption windows may use spare space in the shot.
        next_start=float(lines[lines.index(line)+1]['start_seconds']) if line!=lines[-1] else 180
        limit=min(next_start-.12,164 if start<164 else 180)
        if start+actual>limit:raise ValueError(f'{lid}: natural voice exceeds available hold ({actual:.3f}s). Extend timeline; do not speed it up.')
        a*=.34/max(.001,float(np.max(np.abs(a))))
        fade=min(240,len(a)//4);a[:fade]*=np.linspace(0,1,fade);a[-fade:]*=np.linspace(1,0,fade)
        add(dest,a,start);write_wav(OUT/'speech'/f'{lid}.wav',a)
        caption_end=max(end,start+actual)
        report.append(dict(id=lid,speaker=line['speaker'],start=start,target_end=end,actual_end=round(start+actual,5),caption_end=round(caption_end,5),reused='reuse ' in line['source'],source=line['source'],provider=('original teaser' if line['source'].startswith('reuse ') else 'elevenlabs' if 'ElevenLabs' in line['source'] else 'macos')))
        subs.append((start,caption_end,line['text']))
        print('Speech',lid,line['speaker'],f'{actual:.2f}s',flush=True)
    def stamp(t):
        ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    (OUT/'captions.srt').write_text('\n\n'.join(f'{i}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(subs,1))+'\n')
    (OUT/'speech/timing.json').write_text(json.dumps(report,indent=2));write_wav(OUT/'stems/dialogue.wav',dest)
    return dest,report

def sound(lines,dialogue):
    N=180*SR;stems={}
    sf=Path.home()/'Library/Audio/Sounds/Banks/GeneralUser-GS/GeneralUser-GS.sf2'
    for staff in ('ukulele','piano','strings','brass'):
        mid=OUT/'score'/f'{staff}.mid';p=OUT/'score'/f'{staff}-raw.wav'
        if not p.exists():run(['fluidsynth','-ni','-R','0','-C','0','-r',str(SR),'-g','0.55','-F',p,sf,mid],stdout=subprocess.DEVNULL)
        a=load_audio(p);a=np.pad(a[:N],(0,max(0,N-len(a))))
        gain={'ukulele':2.0,'piano':.22,'strings':.32,'brass':.44}[staff]
        a*=gain
        if staff in ('strings','brass'):
            t=np.arange(N,dtype=np.float32)/SR;a*=np.where(t<164, .35+.65*np.clip((t-62)/102,0,1),1)
        stems[staff]=a
    bass=np.zeros(N,np.float32)
    for e in EVENTS['bass']:
        dur=e['d'];t=np.arange(round(dur*SR),dtype=np.float32)/SR;f=440*2**((e['notes'][0]-69)/12)
        env=(1-np.exp(-t/.018))*np.exp(-t/(1.2 if e['t']>=166 else .35))
        if len(env)>240:env[-240:]*=np.linspace(1,0,240)
        amp=.14*(e['v']/100)**1.4
        a=amp*env*(np.sin(2*np.pi*f*t)+.48*np.sin(2*np.pi*2*f*t)+.15*np.sin(2*np.pi*3*f*t))
        add(bass,a,e['t'])
    stems['bass']=bass
    rng=np.random.default_rng(2631);percussion=np.zeros(N,np.float32)
    for e in EVENTS['percussion']:
        t=np.arange(int(.22*SR),dtype=np.float32)/SR
        a=rng.normal(0,1,len(t)).astype(np.float32);a=np.convolve(a,np.ones(12,dtype=np.float32)/12,mode='same')
        a*=np.exp(-t/.035)*.08*(e['v']/90)
        add(percussion,a,e['t'])
    stems['percussion']=percussion
    effects=np.zeros(N,np.float32)
    t=np.arange(6*SR,dtype=np.float32)/SR
    motor=(rng.normal(0,1,len(t)).astype(np.float32)*.018+np.sin(2*np.pi*93*t)*.012)*(0.55+.45*np.sin(2*np.pi*13*t)**2)
    motor[:2400]*=np.linspace(0,1,2400);motor[-2400:]*=np.linspace(1,0,2400);add(effects,motor,88)
    t=np.arange(int(.5*SR),dtype=np.float32)/SR
    notification=.055*(np.sin(2*np.pi*660*t)+.5*np.sin(2*np.pi*990*t))*np.exp(-t/ .12)*(1-np.exp(-t/.002));add(effects,notification,175)
    stems['effects']=effects
    ambience=rng.normal(0,.00028,N).astype(np.float32);ambience[164*SR:170*SR]=0;stems['ambience']=ambience
    duck=np.ones(N,np.float32)
    for line in lines:
        a=max(0,int((float(line['start_seconds'])-.08)*SR));b=min(N,int((float(line['end_seconds'])+.15)*SR));duck[a:b]=.28
    # Smooth duck envelope without a heavyweight signal-processing dependency.
    idx=np.arange(0,N,240);coarse=duck[idx]
    for _ in range(4):coarse=np.convolve(coarse,[.2,.6,.2],mode='same')
    duck=np.interp(np.arange(N),idx,coarse).astype(np.float32)
    mix=dialogue.copy()
    for name,a in stems.items():
        a[164*SR:166*SR]=0
        if name not in ('effects','ambience'):
            if name!='ukulele':a*=duck
            a[170*SR:]=0
            # Title is a single attack; force tails down smoothly before the room returns.
            tail=np.arange(4*SR,dtype=np.float32)/SR
            a[166*SR:170*SR]*=np.exp(-tail/1.0)
            a[170*SR-2400:170*SR]*=np.linspace(1,0,2400)
        write_wav(OUT/'stems'/f'{name}.wav',a);mix+=a
    mix[164*SR:166*SR]=0
    peak=float(np.max(np.abs(mix)));gain=.82/max(peak,.001);mix*=gain
    write_wav(OUT/'mix.wav',mix)
    (OUT/'mix.json').write_text(json.dumps({'pre_gain_peak':peak,'master_gain':gain,'samples':N,'sample_rate':SR,'scratch_ukulele_timbre':'GeneralUser GS nylon guitar, temporary'},indent=2))
    return mix

def video(rows, only=None):
    mappings={
    'T04':('clips/v3/*shot05-*.mp4',0,'scale=1280:1280,crop=1280:720:0:280'),
    'T05':('clips/v4/*fielder-reaction-*.mp4',2,'scale=1280:1920,crop=1280:720:0:467'),
    'T06':('clips/v4/*fielder-reaction-*.mp4',2,'scale=1280:1920,crop=1280:720:0:467'),
    'T07':('clips/v4/*fielder-reaction-*.mp4',2,'scale=1280:1920,crop=1280:720:0:467'),
    'T16':('clips/inserts/*food-bank-*.mp4',1,'scale=1280:720'),
    'T17':('clips/inserts/*empty-lot-after-*.mp4',2,'scale=1280:720'),
    'T32':('clips/inserts/*demolition-*.mp4',3,'scale=1280:720')}
    enc=['-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','24','-an']
    for r in rows:
        n=r['segment'];dur=float(r['duration_seconds']);p=OUT/'segments'/f'{n}.mp4'
        if only and n not in only:
            assert p.exists(), 'Missing segment outside requested rebuild: '+n
            continue
        if n in mappings:
            glob,ss,vf=mappings[n];sources=list(ROOT.glob(glob));assert len(sources)==1
            status='REHEARSAL MOCKUP - SAME SOURCE REPEATED' if n in ('T06','T07') else 'EXISTING SOURCE'
            vf+=",drawbox=x=0:y=0:w=iw:h=48:color=black@0.85:t=fill,drawtext=fontfile="+str(FONTS['Bold'])+":text='"+LABEL+"  /  "+n+"  /  "+status+"':fontsize=20:fontcolor=white:x=22:y=13"
            ff(['-ss',str(ss),'-i',sources[0],'-t',str(dur),'-vf',vf,*enc,p])
        elif n=='T24':
            base=Image.open(OUT/'plates/T24.png').convert('RGB');proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1280x720','-framerate','24','-i','-',*enc,str(p)],stdin=subprocess.PIPE)
            # Pull back from the exact stream viewport to the wrapper and full storyboard room.
            for k in range(int(dur*FPS)):
                u=k/(dur*FPS-1);e=u*u*(3-2*u)
                rect=[150*(1-e),195*(1-e),934+(1280-934)*e,636+(720-636)*e]
                frame=base.crop(tuple(round(v) for v in rect)).resize((W,H),Image.Resampling.LANCZOS)
                chrome(frame,r,'PULLBACK MOCKUP');proc.stdin.write(frame.tobytes())
            proc.stdin.close();assert proc.wait()==0
        else:ff(['-loop','1','-framerate','24','-i',OUT/'plates'/f'{n}.png','-t',str(dur),*enc,p])
        print('Picture',n,f'{dur:.3f}s',flush=True)
    (OUT/'concat.txt').write_text(''.join(f"file 'segments/{r['segment']}.mp4'\n" for r in rows))
    ff(['-f','concat','-safe','0','-i',OUT/'concat.txt','-c','copy',OUT/'picture.mp4'])
    subtitles=f"subtitles={OUT/'captions.srt'}:fontsdir={FONTDIR}:force_style='FontName=Liberation Sans,FontSize=22,PrimaryColour=&HFFFFFF,OutlineColour=&H90000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=64'"
    ff(['-i',OUT/'picture.mp4','-i',OUT/'mix.wav','-vf',subtitles,'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-t','180','-movflags','+faststart',OUT/OUTPUT_NAME])

def main():
    global OUT, LABEL, AUDIO_LABEL, OUTPUT_NAME
    parser=argparse.ArgumentParser();parser.add_argument('--voice-pass',action='store_true',help='Write the ElevenLabs principal performance pass into its own D2 directory.');parser.add_argument('--segments',help='Comma-separated changed segments; other existing segments are preserved.');parser.add_argument('--phase',choices=['prepare','audio','video','all'],default='all');args=parser.parse_args()
    if args.voice_pass:
        OUT=ROOT/'build/first-trailer-voice-pass-d2'
        LABEL='VOICE PASS D2'
        AUDIO_LABEL='ELEVENLABS PRINCIPALS / TEMP SUPPORT / STORYBOARDS'
        OUTPUT_NAME='first-trailer-voice-pass-d2.mp4'
    for sub in ('plates','segments','speech','score','stems'): (OUT/sub).mkdir(parents=True,exist_ok=True)
    rows=list(csv.DictReader((HERE/'timeline.csv').open()));lines=list(csv.DictReader((HERE/'dialogue.csv').open()))
    assert len(rows)==40 and sum(float(r['duration_seconds']) for r in rows)==180
    if args.phase in ('prepare','all'):
        p=list(ROOT.glob('clips/inserts/*demolition-*.mp4'))[0]
        ff(['-ss','4','-i',p,'-frames:v','1',OUT/'plates/demolition.jpg'])
        make_plates(rows);compose()
        for staff in EVENTS:midi(staff)
        lily();print('Prepared storyboard plates, notation and MIDI.',flush=True)
    if args.phase in ('audio','all'):
        if not EVENTS['piano']:
            data=json.loads((OUT/'score/events.json').read_text());EVENTS.update(data['events'])
        dialogue,report=speech(lines);sound(lines,dialogue);print('Scratch dialogue and all stems rendered.',flush=True)
    if args.phase in ('video','all'):video(rows,set(args.segments.split(',')) if args.segments else None);print('Animatic export complete.',flush=True)
if __name__=='__main__':main()
