# Question 2 — Engine and controlled improvement

## Application procedure
1. Enter symptoms/chief complaint and illness day, plus available age, sex, history, medicines and allergies. Extra structured findings may be entered; no disease label is needed.
2. Validate patient fields and keep the whole patient record in the model context.
3. Build a character TF-IDF sparse index of canonical retrieval_text and retrieve top 16 cards by cosine similarity. The index is rebuilt deterministically from the JSONL at each call. No embedding-model download is required.
4. Send the same patient context and top-k evidence to the configured existing local/API model. The model selects relevant card IDs and supplies short explanations, clarification questions and diagnostic labels.
5. Validate card IDs/category and render exact canonical actions and medication fields, rather than letting the model invent new dosing instructions.
6. Display patient record, retrieved evidence, four output categories, source titles/versions/PDF positions and missing information. Save complete output, raw model text, hashes, timing and model metadata.

The model remains necessary: it handles symptom-to-evidence relevance and selects the plan; output is not a disease-to-answer lookup. The six stored cases are editable input examples, not hard-coded outputs. New cases use the same code path. Bengali text can be entered, but cross-language retrieval and Bengali output quality have not been validated.

## Baseline
Top matching canonical cards + full patient record + reasonable fixed prompt asking the model to obey all prerequisites, use source-only recommendations and handle unknown fields honestly. The baseline sees all card conditions; it is not deliberately stripped of safeguards. Both modes use common citation/category checks and canonical rendering.

## Improved
One change: a three-valued applicability-checking subsystem evaluates the card's explicit prerequisites and required fields. It annotates evidence before model selection and checks selected cards before rendering them as actionable. Inapplicable actions are withheld; uncertain actions are separated into a clarification section. This pre/post use is one applicability subsystem, not a new model/retriever/corpus.

False prerequisites and true exclusions block a card. Missing essential values give unknown. False AND unknown is false; true OR unknown is true. This is important for cholera's pregnancy exception.

## Hypothesis and falsification
Hypothesis: the checker reduces conditional-treatment and missing-information mistakes, especially C5 and C6.
A result showing no benefit: equal or fewer passes on the preregistered four checks, new omissions caused by over-conservative checking, or additional latency without improved behaviour. The model might not retrieve/select the needed card; a checker cannot fix that automatically.

## Six fixed inputs
C1 suspected dengue; C2 repeated-BP hypertension; C3 outbreak diarrhoea without dehydration; C4 chikungunya-like illness with dengue not excluded; C5 incomplete overlapping fever; C6 is C3 with only pregnancy changed to true.
The source-linked expected checklists are kept outside the retrieval corpus and model prompts. C3/C6 explicitly tests that antibiotic eligibility changes but hydration-based ORS does not. Advice and discharge criteria should still be checked rather than assumed satisfied.

## Run protocol
Review the source-linked checklists BEFORE the final comparison. Configure the actual model. `python experiment.py freeze` records cases, cards, expected checklist, engine and settings. `python experiment.py run` attempts both modes on each case, alternating mode order by case and saving 12 output files. It refuses to overwrite existing final outputs. Failures to connect are recorded as errors, not completed clinical generations.
Manually score key behaviour, citation support, restrictions and handling missing information as PASS/FAIL/NA, with reason and source page. Review the model's free-text explanations too: exact action rendering does not guarantee explanations are true. If a key card was not retrieved, citation correctness alone does not make the output pass.

## Current experiment status
NOT RUN: there is no configured running model in the build environment. No clinical success counts or response times are invented. The package supplies a clearly labelled unrun table template, not twelve fake outputs. Mocked software tests are separate from clinical evaluation and never count as the study.
