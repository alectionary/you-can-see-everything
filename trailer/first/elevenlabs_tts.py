#!/usr/bin/env python3
"""Generate a project line with a recovered ElevenLabs voice; credential stays in memory."""
from pathlib import Path
import argparse,json,subprocess,urllib.request,urllib.error,hashlib,os,sys
HERE=Path(__file__).resolve().parent

def generate(character,text,output,*,speed=None,previous_text=None,next_text=None):
    config=json.loads((HERE/'voices.json').read_text());profile=config['characters'][character]
    credential=config['credential']
    # Environment injection is optional; never read a credential from a repository file.
    key=os.environ.get('ELEVENLABS_API_KEY')
    if not key:
        result=subprocess.run(['security','find-generic-password','-a',credential['account'],'-s',credential['service'],'-w'],capture_output=True)
        if result.returncode:raise RuntimeError('ElevenLabs Keychain entry could not be read.')
        key=result.stdout.decode().strip()
    if not key:raise RuntimeError('ElevenLabs credential is empty.')
    settings=dict(profile['voice_settings'])
    if speed is not None:
        if not .7<=speed<=1.2:raise ValueError('Speech speed must be between 0.7 and 1.2.')
        settings['speed']=speed
    payload={'text':text,'model_id':profile['model_id'],'voice_settings':settings}
    if previous_text is not None:payload['previous_text']=previous_text
    if next_text is not None:payload['next_text']=next_text
    output=Path(output);metadata=output.with_suffix('.json')
    signature=hashlib.sha256(json.dumps({'voice_id':profile['voice_id'],**payload},sort_keys=True).encode()).hexdigest()
    if output.exists():
        if metadata.exists() and json.loads(metadata.read_text()).get('request_signature')==signature:
            print('Using cached generation:',output);return
        raise RuntimeError('Output exists with different or missing provenance; choose a new filename.')
    request=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+profile['voice_id']+'?output_format='+config['output_format'],data=json.dumps(payload).encode(),headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},method='POST')
    try:
        with urllib.request.urlopen(request,timeout=120) as response:
            data=response.read()
            provenance={'character':character,'voice_id':profile['voice_id'],'voice_name':profile['voice_name'],**payload,'output_format':config['output_format'],'request_signature':signature,'request_id':response.headers.get('request-id'),'history_item_id':response.headers.get('history-item-id'),'character_cost_header':response.headers.get('character-cost'),'sha256':hashlib.sha256(data).hexdigest()}
    except urllib.error.HTTPError as e:
        body=json.loads(e.read());detail=body.get('detail',{})
        code=detail.get('status','request_failed') if isinstance(detail,dict) else 'request_failed'
        raise RuntimeError(f'ElevenLabs HTTP {e.code}: {code}') from None
    if len(data)<1000:raise RuntimeError('Unexpectedly short ElevenLabs audio response.')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(data);metadata.write_text(json.dumps(provenance,indent=2)+'\n')
    print(f'Generated {character}: {len(text)} characters, {len(data)} bytes -> {output}')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--character',required=True,choices=['DAN','ROY','FIELDER']);p.add_argument('--text',required=True);p.add_argument('--output',required=True)
    p.add_argument('--speed',type=float);p.add_argument('--previous-text');p.add_argument('--next-text')
    args=p.parse_args()
    try:generate(args.character,args.text,args.output,speed=args.speed,previous_text=args.previous_text,next_text=args.next_text)
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
