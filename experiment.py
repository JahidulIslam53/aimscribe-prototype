import json,csv,argparse,os
from core import ROOT,run,sha,PROMPT
parser=argparse.ArgumentParser();parser.add_argument('action',choices=['freeze','run','summary']);args=parser.parse_args()
paths=['data/cases.json','data/cards.jsonl','evaluation/checklists.json','core.py']
def hashes():return {p:sha((ROOT/p).read_text(encoding='utf-8')) for p in paths}
cases=json.loads((ROOT/'data/cases.json').read_text(encoding='utf-8'))
if args.action=='freeze':
    settings={k:os.getenv(k,'') for k in ['MODEL_BASE_URL','MODEL_NAME','MODEL_TEMPERATURE','TOP_K']}
    if not settings['MODEL_NAME']:raise ValueError('Configure the actual model before freezing.')
    frozen={'hashes':hashes(),'settings':settings,'prompt_sha256':sha(PROMPT)}
    (ROOT/'evaluation/freeze.json').write_text(json.dumps(frozen,indent=2))
    print('Cases, expected behaviours, cards, engine and model settings frozen. No expected answers enter retrieval/model prompts.')
elif args.action=='run':
    f=ROOT/'evaluation/freeze.json'
    if not f.exists():raise ValueError('Run freeze first after reviewing the expected checklists.')
    frozen=json.loads(f.read_text())
    if frozen['hashes']!=hashes():raise ValueError('Frozen files changed. Preserve old study and explicitly start a new version.')
    if any(os.getenv(k,'')!=v for k,v in frozen['settings'].items()):raise ValueError('Model settings changed after freeze')
    folder=ROOT/'evaluation/outputs';folder.mkdir(exist_ok=True)
    if list(folder.glob('*.json')):raise ValueError('Outputs already exist. Do not overwrite; archive study and document a new run.')
    rows=[]
    for i,case in enumerate(cases):
        for mode in (['baseline','improved'] if i%2==0 else ['improved','baseline']):
            error=''
            try: out=run(case['patient'],mode)
            except Exception as e: error=str(e);out={'error':error}
            out.update(case_id=case['case_id'],mode=mode)
            (folder/(case['case_id']+'_'+mode+'.json')).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
            rows.append(dict(case_id=case['case_id'],mode=mode,key_behaviour='NOT_REVIEWED',citation_support='NOT_REVIEWED',restrictions='NOT_REVIEWED',missing_information='NOT_REVIEWED',elapsed_seconds=out.get('elapsed_seconds',''),failure_note=error,reason_and_source_page=''))
    with (ROOT/'evaluation/results.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print('Saved 12 attempts. API failures are not valid clinical outputs. Review all outputs and source evidence manually.')
else:
    path=ROOT/'evaluation/results.csv'
    if not path.exists():raise ValueError('No actual results yet')
    rows=list(csv.DictReader(path.open(encoding='utf-8')))
    for mode in ['baseline','improved']:
        group=[r for r in rows if r['mode']==mode]
        for check in ['key_behaviour','citation_support','restrictions','missing_information']:
            counts={v:sum(r[check]==v for r in group) for v in ['PASS','FAIL','NA','NOT_REVIEWED']}
            print(mode,check,counts,'passes/applicable',str(counts['PASS'])+'/'+str(counts['PASS']+counts['FAIL']))
