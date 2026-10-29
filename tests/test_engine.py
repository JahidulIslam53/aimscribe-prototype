import unittest,json
from core import evaluate,applicability,load_cards,run,retrieve,validate_patient,ROOT,CATEGORIES
class TestEngine(unittest.TestCase):
    def test_unknown_not_false(self):self.assertIsNone(evaluate({'field':'pregnant','op':'eq','value':False},{}))
    def test_any_true_wins_unknown(self):self.assertTrue(evaluate({'any':[{'field':'pregnant','op':'eq','value':True},{'field':'elderly','op':'eq','value':True}]},{'pregnant':True}))
    def test_all_false_wins_unknown(self):self.assertFalse(evaluate({'all':[{'field':'pregnant','op':'eq','value':True},{'field':'elderly','op':'eq','value':True}]},{'pregnant':False}))
    def test_abx_exception(self):
        c=next(c for c in load_cards() if c['card_id']=='CHOL-MED-ABX')
        self.assertEqual(applicability(c,{'pregnant':True,'hydration_class':'none','elderly':False,'allergies':[],'current_medicines':[]})['status'],'applicable')
        self.assertEqual(applicability(c,{'pregnant':False,'hydration_class':'none','elderly':False,'allergies':[],'current_medicines':[]})['status'],'inapplicable')
    def test_card_ids_unique(self):
        ids=[c['card_id'] for c in load_cards()];self.assertEqual(len(ids),len(set(ids)))
    def test_coverage(self):
        for disease in ['dengue','hypertension','cholera','chikungunya']:
            self.assertEqual(set(c['category'] for c in load_cards() if c['disease']==disease),set(CATEGORIES))
    def test_evidence_not_empty(self):
        for c in load_cards():
            for s in c['sources']:self.assertTrue(s['evidence_passage']);self.assertGreater(s['pdf_page'],0)
    def test_no_fabricated_chik_pages(self):
        self.assertTrue(all(s['pdf_page']<=23 for c in load_cards() if c['disease']=='chikungunya' for s in c['sources']))
    def test_invalid_types(self):
        with self.assertRaises(ValueError):validate_patient({'symptoms':'fever','pregnant':'no'})
    def test_six_cases_and_one_change(self):
        cases=json.loads((ROOT/'data/cases.json').read_text(encoding='utf-8'));self.assertEqual(len(cases),6)
        a,b=cases[2]['patient'],cases[5]['patient'];self.assertEqual([k for k in a if a[k]!=b[k]],['pregnant'])
    def test_mocked_model_pipeline_is_not_clinical_evaluation(self):
        p={'symptoms':'watery diarrhoea outbreak','age_years':30,'hydration_class':'none','can_drink_safely':True,'pregnant':True,'elderly':False,'current_medicines':[],'allergies':[]}
        retrieved=retrieve(p,load_cards(),16);ids={x['card']['card_id'] for x in retrieved}
        self.assertIn('CHOL-MED-A',ids)
        def mock(messages):
            response={k:[] for k in CATEGORIES};response['medication_planning']=[{'card_id':'CHOL-MED-A','reason':'software test only'}]
            return json.dumps(response),{'model':'MOCK-NOT-A-CLINICAL-RESULT'}
        out=run(p,'improved',caller=mock);self.assertTrue(out['rendered']['medication_planning'])
if __name__=='__main__':unittest.main()
