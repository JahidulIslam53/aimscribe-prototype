"""Run once from the AIMScribe project directory. No API key required by this patch."""
from pathlib import Path
import ast
import datetime

REPLACEMENT = "def model_call(messages):\n    import urllib.error\n    import random\n    name=os.getenv('MODEL_NAME','').strip()\n    if not name:\n        raise RuntimeError('MODEL_NAME is not configured. Set .env; no fake model response is provided.')\n    base=os.getenv('MODEL_BASE_URL','http://localhost:11434/v1').rstrip('/')\n    key=os.getenv('MODEL_API_KEY','')\n    body={'model':name,'messages':messages,'temperature':float(os.getenv('MODEL_TEMPERATURE','0'))}\n    headers={'Content-Type':'application/json'}\n    if key: headers['Authorization']='Bearer '+key\n    payload=json.dumps(body).encode()\n    started=time.perf_counter()\n    history=[]\n    def safe(value):\n        value=str(value)\n        return value.replace(key,'[API_KEY_HIDDEN]') if key else value\n    for attempt in range(1,4):\n        req=urllib.request.Request(base+'/chat/completions',data=payload,headers=headers)\n        try:\n            with urllib.request.urlopen(req,timeout=90) as response:\n                result=json.load(response)\n            text=result['choices'][0]['message'].get('content')\n            if not isinstance(text,str):\n                raise RuntimeError('Provider returned no text content. Inspect response format; no answer was fabricated.')\n            return text,{\n                'requested_model':name,'returned_model':result.get('model'),\n                'temperature':body['temperature'],'usage':result.get('usage'),\n                'model_seconds':time.perf_counter()-started,'base_url':base,\n                'attempts':attempt,'retry_history':history,\n                'retry_policy':'Up to 3 attempts; retry HTTP 502/503/504 and timeouts; 90-second network timeout per attempt. Same request/model on every attempt.',\n                'usage_note':'Usage is the successful response only. Provider processing/billing for failed attempts is unknown.'\n            }\n        except urllib.error.HTTPError as error:\n            details=safe(error.read().decode('utf-8',errors='replace'))[:2500]\n            transient=error.code in (502,503,504)\n            history.append({'attempt':attempt,'http_status':error.code,'details':details})\n            if not transient or attempt==3:\n                raise RuntimeError(\n                    'API request failed after '+str(attempt)+' attempt(s). HTTP '+str(error.code)+\n                    '. Provider details: '+details+\n                    (' Temporary provider failure persisted; no clinical output was produced.' if transient else '')\n                ) from None\n            delay=(5 if attempt==1 else 15)+random.uniform(0,2)\n            history[-1]['wait_seconds']=round(delay,2)\n            print('API temporary HTTP '+str(error.code)+'. Retrying '+str(attempt+1)+'/3 after '+str(round(delay,1))+' seconds.',flush=True)\n            time.sleep(delay)\n        except (TimeoutError,urllib.error.URLError) as error:\n            details=safe(error)\n            history.append({'attempt':attempt,'network_error':details})\n            if attempt==3:\n                raise RuntimeError('API network request failed after 3 attempts: '+details+'. No clinical output was produced.') from None\n            delay=(5 if attempt==1 else 15)+random.uniform(0,2)\n            history[-1]['wait_seconds']=round(delay,2)\n            print('API network delay. Retrying '+str(attempt+1)+'/3 after '+str(round(delay,1))+' seconds.',flush=True)\n            time.sleep(delay)\n"

def main():
    target=Path(__file__).resolve().parent/'core.py'
    if not target.exists():
        raise SystemExit('Place this patch file in the same folder as core.py and app.py, then run again.')
    source=target.read_text(encoding='utf-8')
    tree=ast.parse(source)
    matches=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='model_call']
    if len(matches)!=1:
        raise SystemExit('Expected exactly one model_call function. No file changed.')
    node=matches[0]
    lines=source.splitlines(keepends=True)
    updated = ''.join(lines[:node.lineno-1]) + REPLACEMENT + chr(10) + ''.join(lines[node.end_lineno:])
    ast.parse(updated)
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup=target.with_name('core_before_retry_'+stamp+'.py.bak')
    backup.write_text(source,encoding='utf-8')
    target.write_text(updated,encoding='utf-8')
    print('PATCH APPLIED. core.py now uses bounded retries and detailed provider errors.')
    print('Backup:',backup.name)
    print('No patient data, cards, model name, prompt, retrieval or .env were changed.')
    print('Retry settings apply equally to baseline and improved. Do not patch during a frozen experiment.')
    print('Now rerun software tests, then restart Streamlit. This does not guarantee Google server availability.')

if __name__=='__main__':
    main()
