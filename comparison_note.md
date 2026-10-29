# Comparison note (final frozen run)
Weakness: the baseline may overlook a prerequisite or assume an unknown value is negative, despite a reasonable source-grounding prompt.
Change: add a three-valued applicability subsystem to the same top-k cards and model. This supplies annotations and checks selected actions. No extra model call is added.
Hypothesis: improved restriction/missing-information performance, particularly C5 and C6. No benefit means unchanged/worse check counts or extra latency without better behaviour. Overblocking is also a possible negative outcome.
Controls: identical model, temperature, top-k=16, source-card corpus, patient cases and system prompt. Freeze files/settings before final runs. Expected checklists stay out of prompts and index.

## Results

The final frozen experiment generated 12 attempts across six self-authored cases and two modes.

Eight attempts produced valid model outputs: C1–C4 in both baseline and improved modes. All eight valid outputs received PASS for key behaviour, citation support, restrictions, and missing-information handling in manual source-linked review.

Four attempts failed before producing model output: C5_incomplete and C6_cholera_pregnant, in both modes. These failed with Gemini API HTTP 429 RESOURCE_EXHAUSTED input-token quota errors. They were scored NA rather than treated as clinical successes or clinical failures.

For the eight valid outputs, both baseline and improved modes met the pre-specified checklist behaviours. The improved mode added applicability metadata and, in C1, considered chikungunya acute-phase test timing. No clinical failure, unsupported medication dose, or major restriction violation was observed in this small comparison.

This is a small, self-authored six-case comparison and does not establish broad clinical accuracy. C5 and C6 could not be evaluated because of provider quota failures. The comparison is therefore based on eight valid outputs from C1–C4.
## Known limitations and next steps

Retrieval may omit a crucial card, so applicability checking cannot recover missing evidence. A likely cause could be lexical cross-language mismatch. An alternative explanation for a future observed difference is model variability rather than the checker.

Next test: preserve all runs, repeat order-balanced generation, inspect retrieved-card coverage, and add independently authored Bengali/code-switched cases. If all checks pass, show C6 as the conditional challenge and state the untested image-only algorithm, paediatric dosing and real-clinic outcomes.