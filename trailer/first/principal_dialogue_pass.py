"""Render only missing principal-role lines, reusing matching samples and teaser audio."""
from pathlib import Path
import csv,json,hashlib,importlib.util,subprocess,urllib.request,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('eleven',HERE/'elevenlabs_tts.py');tts=importlib.util.module_from_spec(spec);spec.loader.exec_module(tts)
config=json.loads((HERE/'voices.json').read_text());rows=list(csv.DictReader((HERE/'dialogue.csv').open()));fields=list(rows[0]);entries=[];missing=[]
for row in rows:
    role=row['speaker']
    if role not in config['characters']:continue
    if row['source'].startswith('reuse '):
        entries.append({'line_id':row['line_id'],'role':role,'text':row['text'],'path':row['source'].split(' ',1)[1].split(';',1)[0],'status':'original teaser recording'});continue
    profile=config['characters'][role]
    payload={'voice_id':profile['voice_id'],'text':row['text'],'model_id':profile['model_id'],'voice_settings':profile['voice_settings']}
    signature=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    found=None
    # Preserve an explicitly selected take, including per-line delivery settings.
    if row['source'].startswith('file '):
        active=ROOT/row['source'].split(' ',1)[1].split(';',1)[0];meta=active.with_suffix('.json')
        if active.exists() and meta.exists():
            m=json.loads(meta.read_text())
            saved={k:m[k] for k in ('text','model_id','voice_settings','previous_text','next_text') if k in m}
            saved_signature=hashlib.sha256(json.dumps({'voice_id':m.get('voice_id'),**saved},sort_keys=True).encode()).hexdigest()
            if m.get('text')==row['text'] and m.get('voice_id')==profile['voice_id'] and m.get('model_id')==profile['model_id'] and m.get('request_signature')==saved_signature and m.get('sha256')==hashlib.sha256(active.read_bytes()).hexdigest():found=active
    for meta in (ROOT/'dialogue/first').rglob('*.json'):
        try:m=json.loads(meta.read_text())
        except ValueError:continue
        if not isinstance(m,dict):continue
        candidate=meta.with_suffix('.mp3')
        if found is not None:break
        if m.get('request_signature')==signature and candidate.exists():found=candidate;break
    if found is None:
        found=ROOT/'dialogue/first/principal'/f"{row['line_id']}_{role.lower()}.mp3";missing.append((row,found))
    entries.append({'line_id':row['line_id'],'role':role,'text':row['text'],'path':str(found.relative_to(ROOT)),'voice_id':profile['voice_id'],'model_id':profile['model_id'],'status':'generate' if any(x[0]['line_id']==row['line_id'] for x in missing) else 'matching ElevenLabs recording'})
print('Principal lines:',len(entries),'missing generations:',len(missing),'new text characters:',sum(len(x[0]['text']) for x in missing),flush=True)
# Read quota, keeping the credential out of arguments and saved project files.
import sys
if '--generate' not in sys.argv:
    print('Dry run only. Add --generate to use included credits for missing recordings.');raise SystemExit(0)
c=config['credential'];key=os.environ.get('ELEVENLABS_API_KEY')
if not key:key=subprocess.run(['security','find-generic-password','-a',c['account'],'-s',c['service'],'-w'],capture_output=True,check=True).stdout.decode().strip()
def usage():
    req=urllib.request.Request('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':key})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
before=usage();chars=sum(len(row['text']) for row,_ in missing);remaining=before['character_limit']-before['character_count']
print('Included credits available:',remaining,flush=True)
if chars>remaining:raise SystemExit('Insufficient included credits for this batch; no requests made.')
for row,path in missing:tts.generate(row['speaker'],row['text'],path)
# Update the active sources only after the entire batch is available.
for e in entries:
    if e['status']=='original teaser recording':continue
    path=ROOT/e['path'];assert path.exists()
    e['status']='ElevenLabs recording available';e['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    row=next(x for x in rows if x['line_id']==e['line_id'])
    row['source']='file '+e['path']+'; ElevenLabs '+config['characters'][e['role']]['voice_name'].split(' - ')[0]+', recovered original settings'
with (HERE/'dialogue.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
after=usage()
summary={'principal_lines':len(entries),'new_generations':len(missing),'new_text_characters':chars,'credits_used_this_pass':after['character_count']-before['character_count'],'included_credits_remaining':after['character_limit']-after['character_count'],'roles':{r:config['characters'][r]['voice_name'] for r in config['characters']},'lines':entries,'supporting_roles':'macOS placeholders retained'}
(HERE/'principal-dialogue-pass.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Batch complete; charged credits:',summary['credits_used_this_pass'],'remaining:',summary['included_credits_remaining'],flush=True)
