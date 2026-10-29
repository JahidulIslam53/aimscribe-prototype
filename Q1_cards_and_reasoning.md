# Question 1 — Recommendation cards and reasoning

## What is implemented
The dataset contains 32 source-grounded cards spanning diagnosis, investigations, medication planning and advice across the four protocols. Every card has a stable ID, disease, category, searchable text, prerequisite expression, exclusions, required patient fields, recommended action, missing-information notes and source records. Source records retain exact source title/version, one-based PDF position and extracted supporting page text. Full-page passages were retained for auditability, not as an assertion that all page content belongs to the recommendation. Narrower verified passages are a future refinement.

These are AI-curated research cards, not clinician-approved guidance. The review_status field explicitly says AI_SOURCE_CHECKED_REQUIRES_HUMAN_REVIEW. Do not relabel them as independently clinically validated.

## Field explanations
- card_id: stable citation/lookup key, e.g. CHOL-MED-ABX.
- disease: protocol scope; not required in patient input.
- category: probable_diagnosis, investigations, medication_planning or advice.
- retrieval_text: relevant symptoms, action and reviewed-language terms used by the index.
- prerequisites: nested all/any/not expressions. Leaf comparisons preserve exact conditions. Unknown values are not automatically false.
- exclusions: optional expressions; any true exclusion blocks applicability.
- required_patient_fields: fields that must be known before a patient-specific action is applied.
- missing_information: source gaps such as an unspecified route or duration.
- recommended_action.text: human-readable, source-grounded recommendation with conditions and qualifications.
- recommended_action.medication: name, dose, route, frequency, duration, instructions; unsupported fields are null. Alternative options are distinguished from combinations.
- sources: one or more source facts, with source ID, title, edition, PDF page and evidence passage.
- review_status: provenance of curation, not an automatic approval badge.

## Concrete reasoning challenge: cholera antibiotic eligibility
Source: WHO Clinical tools for cholera treatment facilities, 2024, PDF pages 5, 9 and 11.

Representation A, rejected: attach an antibiotic statement only to the severe-dehydration/Plan-C card. This is compact but implies that only severe dehydration qualifies.

Representation B, implemented: a separate eligibility card uses OR logic:
```
severe dehydration OR pregnant OR elderly
```
Pregnancy and elderly status qualify irrespective of hydration status/treatment plan. The adult options are a linked card, retaining the dose evidence from PDF page 5. Age ≥18 is a conservative scope for this adult-only implementation, not an invented source definition of the older-child boundary. The source does not give a numeric elderly threshold; the prototype accepts a clinician-supplied boolean and does not invent one. Antibiotic route is null because the cited passage does not state it.

Failure example for A: a 30-year-old pregnant patient with acute watery diarrhoea during a declared outbreak and a complete no-dehydration assessment. A hydration-only representation may omit antibiotics. In B, the pregnancy branch is true, so antibiotic planning is eligible while the hydration-based Plan A remains unchanged. This is exactly the C3/C6 pair.

Missing pregnancy is unknown, not nonpregnant. If severe dehydration is already true, an unknown pregnancy field does not invalidate the OR result, although other required drug-safety details still matter.

## Disease policies must stay distinct
Dengue PDF page 47 specifies paracetamol maximum 3 g/day. Chikungunya PDF pages 18–19 list up to 1000 mg four times daily in persons without pre-existing liver/kidney disease; PDF page 18 says to manage suspected chikungunya as dengue until dengue is ruled out. These must not be merged into a universal fever-dose card. The isolated chikungunya dose card is restricted to cases with dengue excluded. The prototype is conservative and does not generate a per-dose dengue schedule that the cited passage does not supply.

## Source limitations
- Chikungunya supplied PDF: 23 pages, so assigned PDF positions 26–27 cannot be read or cited. Actual positions 11–22 are used and the gap is explicit.
- Hypertension PDF page 64 is largely an embedded algorithm image. The actual embedded figure is preserved for inspection. No full visual transcription is claimed, so its complete stepwise dose algorithm is NOT implemented.
- Additional hypertension PDF pages 55–57 support lifestyle advice; page 60 supports pregnancy medication restrictions. These extra pages are explicitly recorded, as permitted by the assessment.
- Cholera page 5 and page 9 have some differing age/weight table boundaries; page 5 has a Plan-A four-hour label, whereas page 11 explicitly describes after-each-stool dosing. The adult Plan-A card cites page 11. The prototype does not silently combine tables.
- Cholera page 12 quick-reference volumes should not be equated automatically to exact weight-based calculations. It is retained in source evidence but not implemented as a universal dose calculator.
- Zinc text at exactly six months and its upper-age applicability require clarification; no blanket adult zinc recommendation was created. PDF page 14 explicitly refers to paediatric zinc completion.
