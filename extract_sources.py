import json,hashlib,shutil
from pathlib import Path
from pypdf import PdfReader
from core import ROOT
manifest=json.loads((ROOT/'data/source_manifest.json').read_text())
for disease,sp in manifest.items():
    path=ROOT/'protocols'/sp['filename']
    if not path.exists(): print(disease,'PDF missing; add exact original');continue
    if hashlib.sha256(path.read_bytes()).hexdigest()!=sp['sha256']:raise ValueError(disease+': source differs from supplied copy; do not reuse old page citations without review')
    reader=PdfReader(path)
    for n in sp['assigned']+sp['extra']:
        if n>len(reader.pages): print(disease,'assigned page absent:',n);continue
        folder=ROOT/'reextracted'/disease;folder.mkdir(parents=True,exist_ok=True)
        (folder/f'pdf_{n}.txt').write_text(reader.pages[n-1].extract_text(),encoding='utf-8')
print('Text re-extraction is not visual verification. Inspect original tables/images and footnotes.')
