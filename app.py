import json
import streamlit as st
from core import ROOT,load_cards,run,model_call
st.set_page_config(page_title='AIMScribe — protocol prototype',layout='wide')
st.title('AIMScribe | Evidence-grounded clinical NLP')
st.warning('Fictional cases only. AI-curated evidence requires human checking. Not validated for clinical care or autonomous prescribing.')
mode=st.radio('Mode',['baseline','improved'],horizontal=True)
st.caption('Same corpus, retrieval and model. Improved adds three-valued applicability checking. No model outputs or clinical experiment results are precomputed.')
with st.expander('Source audit and important gaps',expanded=False):
    st.json(json.loads((ROOT/'data/source_manifest.json').read_text()))
    st.error('Chikungunya PDF has 23 pages; assigned PDF pages 26–27 are absent. Hypertension page-64 image must be visually transcribed and reviewed before claiming full algorithm coverage.')
    st.image(str(ROOT/'evidence/hypertension_pdf64_algorithm.jpg'),caption='Exact embedded figure from hypertension PDF page 64. Preserved for human inspection; no OCR transcription is claimed.')
ack=st.checkbox('I understand this is a source-grounded research prototype, not a verified prescription system.')
cases=json.loads((ROOT/'data/cases.json').read_text(encoding='utf-8'))
choice=st.selectbox('Start with a fictional case or enter a new case',['New']+[x['case_id'] for x in cases])
p=next((x['patient'] for x in cases if x['case_id']==choice),{'symptoms':'','age_years':None,'illness_day':None,'sex':None,'pregnant':None,'current_medicines':None,'allergies':None,'history':''})
st.caption('No disease label is required. Symptoms can be Bengali or English; multilingual quality is not established. All fields remain editable. Unknown = null, not false. Hydration classification is a clinician-entered assessment, not inferred automatically.')
text=st.text_area('Patient context — editable JSON',json.dumps(p,indent=2,ensure_ascii=False),height=420,key=choice)
if st.button('Test configured model'):
    try:
        out,meta=model_call([{'role':'user','content':'Reply OK only.'}]);st.write(out);st.json(meta)
    except Exception as e: st.error(str(e))
if st.button('Generate patient-specific evidence plan',type='primary',disabled=not ack):
    try:
        with st.spinner('Retrieving cards and asking the configured model...'): result=run(json.loads(text),mode)
        st.subheader('Patient information');st.json(result['patient'])
        with st.expander('Retrieved evidence',expanded=False):
            for row in result['retrieved']:
                st.write(row['card']['card_id'],f"score={row['score']:.3f}");st.json(row['card'])
        for cat,recs in result['rendered'].items():
            st.subheader(cat.replace('_',' ').title())
            if not recs: st.write('No supported recommendation selected; inspect clarifications and evidence.')
            for rec in recs:
                st.write(rec['recommendation']['text'])
                if rec['recommendation']['medication']: st.json(rec['recommendation']['medication'])
                st.caption('Model selection reason (must be checked): '+rec['model_reason'])
                for src in rec['sources']:
                    st.caption(f"{rec['card_id']} | {src['title']} | {src['version']} | PDF p. {src['pdf_page']}")
                with st.expander('Supporting passages '+rec['card_id']): st.json(rec['sources'])
        st.subheader('Missing information / questions');st.write(result.get('clarifications',[]))
        with st.expander('Conditional or withheld actions'): st.json(result['blocked_or_conditional'])
        st.subheader('Limitations');st.write(result.get('limitations',[]))
        if result['errors']: st.error(str(result['errors']))
        st.caption(f"Elapsed {result['elapsed_seconds']:.2f} s")
        st.download_button('Save full output and evidence',json.dumps(result,indent=2,ensure_ascii=False),'case_output.json','application/json')
    except Exception as e: st.error(str(e))
