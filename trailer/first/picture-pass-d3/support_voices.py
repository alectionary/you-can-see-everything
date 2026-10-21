"""Generate the nine supporting lines without changing the principal voice registry."""
from pathlib import Path
import csv,json,subprocess,urllib.request,hashlib
ROOT=Path('/Users/anonymous/Documents/you-can-see-anything-teaser')
HERE=ROOT/'trailer/first/picture-pass-d3'
roles={
 'OFFSCREEN DIRECTOR':('JBFqnCBsd6RMkjVDRZzb','George'),
 'ROY CANDIDATE A':('bIHbv24MWmeRgasZH58o','Will'),
 'ROY CANDIDATE B':('CwhRBWXzGAHq8TQ4Fs17','Roger'),
 'ROY CANDIDATE C':('onwK4e9ZLuTAKqWW03F9','Daniel'),
 'COMMUNICATIONS':('EXAVITQu4vr4xnSDxMaL','Sarah'),
 'OFFSCREEN CREW':('IKne3meq5aSn9XLyUdCD','Charlie'),
 'EDITOR':('XrExE9yKIg1WjnnlVkGX','Matilda')}
config=json.loads((ROOT/'trailer/first/voices.json').read_text());c=config['credential']
key=subprocess.run(['security','find-generic-password','-a',c['account'],'-s',c['service'],'-w'],capture_output=True,check=True).stdout.decode().strip()
def usage():
 req=urllib.request.Request('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':key})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
before=usage();rows=list(csv.DictReader((ROOT/'build/first-trailer-voice-pass-d2/dialogue.csv').open()));entries=[]
assert before['character_limit']-before['character_count']>=sum(len(r['text']) for r in rows if r['speaker'] in roles)
for row in rows:
 if row['speaker'] not in roles:continue
 voice,name=roles[row['speaker']];path=ROOT/'dialogue/first/support'/f"{row['line_id']}.mp3";meta=path.with_suffix('.json')
 settings={'stability':.55,'similarity_boost':.75,'speed':1.0,'style':0.0,'use_speaker_boost':True}
 payload={'text':row['text'],'model_id':'eleven_multilingual_v2','voice_settings':settings}
 signature=hashlib.sha256(json.dumps({'voice_id':voice,**payload},sort_keys=True).encode()).hexdigest()
 if path.exists():
  m=json.loads(meta.read_text());assert m['request_signature']==signature
 else:
  req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+voice+'?output_format=mp3_44100_128',data=json.dumps(payload).encode(),headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},method='POST')
  with urllib.request.urlopen(req,timeout=120) as response:
   data=response.read();m={'character':row['speaker'],'voice_id':voice,'voice_name':name,**payload,'output_format':'mp3_44100_128','request_signature':signature,'request_id':response.headers.get('request-id'),'history_item_id':response.headers.get('history-item-id'),'character_cost_header':response.headers.get('character-cost'),'sha256':hashlib.sha256(data).hexdigest()}
  assert len(data)>1000
  path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);meta.write_text(json.dumps(m,indent=2)+'\n')
 row['source']='file '+str(path.relative_to(ROOT))+'; ElevenLabs '+name+', supporting cast'
 entries.append({'line_id':row['line_id'],'role':row['speaker'],'voice':name,'voice_id':voice,'path':str(path.relative_to(ROOT)),'sha256':m['sha256']})
 print('Ready',row['line_id'],row['speaker'],name,flush=True)
with (HERE/'dialogue.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
after=usage();report={'lines':entries,'credits_used':after['character_count']-before['character_count'],'credits_remaining':after['character_limit']-after['character_count'],'principal_sources':'Preserved exactly from accepted D2-r1 dialogue.csv'}
(HERE/'support-voices.json').write_text(json.dumps(report,indent=2)+'\n')
print('Complete',report['credits_used'],'credits,',report['credits_remaining'],'remaining',flush=True)
