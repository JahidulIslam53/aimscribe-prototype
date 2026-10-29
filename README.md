# AIMScribe revised source-grounded implementation

## Read this status first

This package includes 32 canonical cards based on the uploaded protocols, actual page extractions, source hashes, six source-linked fictional cases/checklists, two-mode application code, an experiment runner, architecture, draft paper summary, presentation slides and an interview guide.

The final frozen experiment was run with Google Gemini API using `gemini-3.5-flash-lite`, temperature 0 and TOP_K 16. It generated 12 attempts across six cases and two modes.

Eight attempts produced valid outputs: C1–C4 in both baseline and improved modes. All eight valid outputs passed the four manual source-linked checks. Four attempts—C5_incomplete and C6_cholera_pregnant in both modes—failed with Gemini API HTTP 429 quota errors and were scored NA, not as clinical pass or clinical failure.

The exact missing chikungunya pages and untranscribed hypertension algorithm are documented. All cards are AI-curated and require source review/appropriate clinical supervision. No broad clinical validation is claimed.

## Install and launch

Use Python 3.10+ and a terminal in this project directory:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then add your own provider API key. A real key is not included. The final evaluation used Google Gemini API with `gemini-3.5-flash-lite`, temperature 0 and TOP_K 16. Hosted inference may cost money; use fictional cases only. Never put a real API key in the submitted ZIP.

```bash
streamlit run app.py
```

Click **Test configured model**. The app makes a real HTTP model call; it does not return canned examples. Editable JSON preserves unknown versus false. No disease name is required. The model selects card IDs and explanations; canonical action text is rendered from evidence.

## Source positions and gaps
- Dengue: exact PDF positions 26–28, 37–41, 45–48, fifth edition 2025.
- Hypertension: exact PDF positions 46–52, 64–65, second edition November 2023. Printed-page numbers differ. Page-64 embedded algorithm is saved as an image for human inspection, but full visual transcription/implementation is pending. No dose sequence was fabricated.
- Cholera: exact PDF positions 5–14, WHO 2024.
- Chikungunya: this supplied 2017 PDF has only 23 pages. Positions 11–22 exist; positions 26–27 do not. Ask for the intended copy or clarification. Do not silently remap.
- Extra hypertension pages 55–57 support lifestyle advice; page 60 supports pregnancy medicine restrictions. These are recorded in the manifest.
The requested 45 positions therefore include two unavailable positions; 43 assigned positions exist in these supplied copies. An existing page can still contain image text that needs visual review.
Original PDFs are not redistributed in this ZIP. If needed, place your copies under protocols/ using the original filenames in the manifest and run `python extract_sources.py` to verify source hashes and rebuild extraction.

## Controlled comparison

1. Review canonical actions, passages, conditions, cases and `evaluation/checklists.json` against the original PDFs.
2. Configure the model and complete development testing before the final comparison.
3. `python experiment.py freeze`
4. `python experiment.py run`
5. Manually review all twelve actual outputs. Complete `evaluation/results.csv` with PASS, FAIL or NA plus a reason and PDF page for each check. API errors are not successful clinical outputs.
6. `python experiment.py summary` reports counts/denominators for scored applicable checks; `NOT_REVIEWED` and `NA` are separate.
7. `docs/comparison_note.md` and the slides have been updated with the actual findings, timing and limitations.

Final result: 8 valid outputs from C1–C4 passed all four applicable checks in both modes. C5 and C6 could not be evaluated because all four attempts failed with HTTP 429 provider quota errors; they were scored NA.

The runner keeps expected checklists out of prompts/index and refuses to overwrite existing outputs. Any rerun should be recorded as a new experiment, never as a quiet replacement of a poor result.

## Files to understand
- core.py: sparse RAG retrieval, model call, JSON validation, three-valued rules, canonical rendering.
- app.py: one editable interface with mode switch and evidence display.
- data/cards.jsonl: 32 cards with explicit conditions, drug fields and source pages.
- data/cases.json and evaluation/checklists.json: six cases and expected behaviours.
- evidence/: exact extracted pages and retained hypertension algorithm image.
- docs/Q1_cards_and_reasoning.md: schema and real cholera exception challenge.
- docs/Q2_engine_and_experiment.md: procedure, baseline/improvement and experiment plan.
- docs/Q3_architecture.md: complete intended architecture and implementation boundaries.
- docs/Q4_paper_summary_DRAFT.md: 200–300-word source-attributed draft; final-article verification pending.
- docs/interview_guide.md: Bengali explanation and 34 likely interview questions.
- presentation.pptx: 12 slides, including final experiment results, model configuration and limitations.
- BUILD_STATUS.json: exact checks run during packaging.

## Tests and limitations
`python -m unittest discover -s tests -v`
Software tests include mocked model selection; they are NOT the clinical comparison. Live Gemini API integration was tested in the final frozen experiment; four C5/C6 attempts failed because of provider HTTP 429 quota limits. RAG retrieval is sparse and not validated for Bengali cross-language use. Whole-page passages can increase token/latency cost. The checker covers encoded rules only; model explanations and diagnostic labels still need manual verification. Hydration classification is clinician-entered, not automatically inferred from sparse symptom text. Paediatric prescribing, dose calculations, OCR, ASR, trained NER, hospital integration and autonomous prescribing are outside the implementation. The assigned paper's final-version figure/table references need the final PDF.

## Final evaluation result

- Total attempts: 12
- Valid model outputs: 8 (C1–C4, baseline and improved)
- API failures: 4 (C5 and C6, baseline and improved)
- Valid outputs passing all four checks: 8/8
- API failures scored: NA
- Model: gemini-3.5-flash-lite
- Temperature: 0
- TOP_K: 16
- Comparison basis: eight valid outputs from C1–C4

## AI disclosure
AI assisted source structuring, code, case/checklist drafts, slides and documentation. Record your own source checks, corrections, actual model, settings, runs and interpretation. Do not claim unperformed human or clinical verification. This is a research demonstration and must not be used as a patient-facing prescription system.
