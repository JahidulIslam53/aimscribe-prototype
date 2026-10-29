# Question 3 — System architecture
```mermaid
flowchart TD
 A[Four supplied PDF protocols] --> B[Implemented: exact-page extraction and source hashes]
 B --> C[Implemented: curated canonical JSONL and supporting passages]
 B --> I[Retained tables and image evidence; manual review required]
 I --> C
 C --> D[Implemented: TF-IDF sparse RAG index]
 P[Implemented: editable patient input and complete context] --> R[Implemented: top-k retrieval]
 D --> R
 R --> M{Mode switch}
 M --> BL[Baseline: original cards and patient context]
 M --> IM[Improved: same cards plus applicability annotations]
 BL --> L[Implemented API connector: existing model selects card IDs]
 IM --> L
 L --> V[Implemented common ID/category checks]
 V --> G[Improved only: same applicability subsystem checks selection]
 V --> O[Baseline canonical renderer]
 G --> O
 O --> UI[Four output categories, evidence, questions, export]
 N[Future: Bengali conversation ASR and clinical NER] --> NC[Future: human verification of entities, negation, units and uncertainty]
 NC --> P
 UI --> F[Future: doctor acceptance/rejection with reasons and source IDs]
 F --> Q[Future: curated feedback review, not automatic rule updates]
 UI --> RX[Future: clinician-approved prescription assembly]
 C --> RX
```

Implemented means written and software-tested to the extent reported in BUILD_STATUS.json. It does not imply that live API integration, visual source review or clinical validation has occurred. The source-card dataset is AI-curated. The full hypertension algorithm is not yet implemented.

## Why this design?
For a small, fixed protocol corpus, JSONL makes conditions and provenance inspectable. Character TF-IDF avoids downloading an embedding model and is fast enough to rebuild. It misses semantic/cross-language matches and can retrieve the wrong protocol. A future retrieval study could compare bilingual dense retrieval, but that is not combined with the current experiment.

Compared with simply chunking PDF text, canonical cards preserve one recommendation and its linked prerequisites, exceptions, timing and source references. This requires manual curation and can introduce transcription mistakes, so retain evidence and review cards against the source.

## New detail changes the plan
Re-run with the complete updated patient record. In C3→C6 only pregnancy changes, so the cholera antibiotic OR rule becomes true while the no-dehydration ORS branch remains unchanged. Do not silently carry forward a prior treatment decision after context changes.

## Model and safety boundaries
The model chooses relevant cards; canonical rendering limits invented action wording. Citation integrity is not evidence entailment. The model can select an irrelevant card, miss a needed card, hallucinate a supporting reason or misclassify a diagnosis. The applicability checker can only evaluate encoded rules and entered structured facts. It cannot prove safe prescribing.

## Future integrations
NER results join the patient record after verification; do not train NER for this assessment. Doctor acceptance/rejection should link case/output/card/source IDs and reason, not automatically rewrite guidelines. Prescription assembly must require a clinician-approved drug selection and complete patient-specific medication fields. Source IDs accompany every stage to preserve traceability.

## Cost/latency trade-off
One model call per case per mode; improved adds no extra LLM call but adds CPU rule checks and prompt annotation tokens. Top-k=16 can produce a large context because full-page passages are retained. Smaller evidence spans after manual review would reduce tokens/latency, but changing spans between modes would confound the comparison. Log actual response time, token usage where available and model/version. Record costs separately if the provider supplies prices. Do not invent cost figures.
