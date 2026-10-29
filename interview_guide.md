# Interview preparation — understand and defend your work

## 60-second introduction (English)
I built a small protocol-grounded clinical recommendation prototype for four conditions. It accepts symptoms rather than requiring a disease label, retrieves canonical recommendation cards and asks an existing model to select relevant evidence. Each recommendation keeps its source edition and PDF position. The baseline uses the same cards and patient context as the improved mode. The improvement is explicit three-valued applicability checking, so missing facts are not treated as negative findings. I evaluate source support and conditional behaviour on six frozen fictional cases rather than claiming clinical accuracy. I also documented source gaps: the supplied chikungunya copy has only 23 pages, and the full hypertension algorithm requires visual transcription.

Do not say you completed live model evaluation until you actually ran it. Replace the last sentence with your true progress during the interview.

## সহজভাবে পুরো কাজ
এটি নতুন করে model train করার কাজ নয়। চারটি guideline থেকে যাচাইযোগ্য recommendation সাজানো হচ্ছে। রোগীর symptoms দিয়ে প্রাসঙ্গিক card খোঁজা হয়, তারপর existing model card বেছে নেয়। কার্ডে treatment-এর শর্ত ও PDF page থাকে। তাই কেন কোনো পরামর্শ এসেছে তা source খুলে দেখানো যায়।

RAG মানে retrieval-augmented generation: আগে প্রাসঙ্গিক evidence খোঁজা, তারপর evidence ও patient context দিয়ে model-এর সাহায্যে উত্তর নির্বাচন করা। Model-এর নিজের জানা কথা guideline-এর বিকল্প নয়।

Canonical card মানে একই structure-এ সাজানো recommendation। যেমন একটি card-এর মধ্যে action, প্রয়োগের শর্ত, কী তথ্য নেই এবং কোন PDF page থেকে এসেছে—সব একসঙ্গে থাকে। Canonical মানে clinically certified নয়।

Baseline-কে ইচ্ছা করে খারাপ করা হয়নি। সেটিও সব conditions ও ভালো prompt পায়। Improved mode-এ অতিরিক্তভাবে code দিয়ে condition true/false/unknown হিসেবে পরীক্ষা হয়। একই model ও retrieval রেখে এ পরিবর্তনের প্রভাব দেখা হয়।

## গুরুত্বপূর্ণ উদাহরণ: C3 ও C6
C3-তে cholera outbreak-এর মধ্যে watery diarrhoea আছে, কিন্তু assessment-এ dehydration নেই। C6-তে অন্য সব একই রেখে শুধু pregnant=true করা হয়েছে। WHO source অনুযায়ী pregnancy থাকলে hydration status যাই হোক antibiotic planning-এর indication হয়। তাই antibiotic eligibility বদলাবে, ORS-এর no-dehydration branch নিজে থেকে বদলাবে না। এই উদাহরণটি PDF pages 5, 9, 11 খুলে দেখাতে পারবেন। এটি demonstration, actual patient prescription নয়।

## Likely questions and defensible answers

1. Why not train a model? The assessment asks for an existing model; training adds cost and does not guarantee protocol fidelity.
2. Why cards rather than raw PDF chunks? A card keeps one action with its prerequisite, exception and source facts; raw chunks can separate a footnote from its table row.
3. Why JSONL? It is inspectable, versionable and easy to validate. One card per line is not a required quota.
4. What is the retriever? Character TF-IDF with cosine similarity over retrieval_text; top-k is 16. It is a sparse RAG index, not a dense embedding vector store.
5. Why not dense retrieval? To keep the prototype small and reproducible without extra downloads. Dense/hybrid retrieval is a separate future comparison.
6. Does Bengali work? The UI accepts Bengali text and some cards contain Bengali cues, but that does not establish reliable cross-language retrieval. We must test Bengali/code-switching explicitly.
7. What does the model actually do? It maps the whole patient context to retrieved evidence and selects card IDs with explanations and questions. Exact action content is rendered from cards.
8. Is this hard-coded? The six cases are examples only. New cases call the same retrieval and model path. The clinical knowledge is a curated dataset, which is expected in RAG.
9. What is the single improvement? An applicability-checking subsystem used before model selection and before improved-mode rendering; the corpus, model and retrieval remain fixed.
10. What does unknown mean? A needed fact was not supplied or cannot be compared. Unknown pregnancy is not false pregnancy.
11. Why three-valued logic? Boolean-only logic can silently treat missing data as absent. True OR unknown remains true; false AND unknown remains false.
12. Why are alternative antibiotics not combined? The source calls one preferred and another alternative. A list of options is not a combination prescription.
13. Why is an antibiotic route null? The cited WHO excerpt does not explicitly state it; general pharmacology knowledge must not fill a source gap in this assessment.
14. What is the paracetamol issue? Dengue page 47 has a 3 g/day maximum. Isolated chikungunya has a different policy with liver/kidney restrictions, and suspected chikungunya must be managed as dengue until ruled out. Do not merge them.
15. How do you know citations support a claim? Open the cited PDF position and compare the action, conditions, table headers and footnotes. A valid card ID alone is not proof.
16. Is everything in the source implemented? No. Scope is demonstrated cases, not every disease pathway. The missing chikungunya pages and image-only hypertension algorithm are explicit gaps.
17. Why not cite printed page 33 for hypertension? Assessment requires PDF position; printed 33 is PDF position 64 in this copy.
18. Can the system confirm diagnoses? Only when source criteria and patient findings justify it. Symptoms alone generally support suspected/possible/probable categories; show the distinction.
19. What are the six cases? One per disease, one incomplete differential case, one single-prerequisite modification of cholera.
20. What is frozen? Case input, expected checklists, cards, engine and model settings. Expected answers never enter prompts or index.
21. What are the four checks? Key expected behaviour, citation support, preservation of restrictions, and honest handling of missing facts.
22. What if improved is worse? Report it. Overblocking, incomplete structured inputs, retrieval gaps or model variability could explain it. A well-run negative result is valid.
23. Is pass rate clinical accuracy? No. It is behaviour-check performance on six self-authored cases, not independent clinical validation.
24. What if a model call fails? Save the error and report failure to produce an output. Do not replace it with a hand-written answer labelled as model output.
25. Does temperature zero guarantee reproducibility? No. Record requested/returned model, settings, hashes and raw outputs; repeat runs to examine variability.
26. How do you measure latency? Wall-clock time around retrieval, model call and rendering/check processing; token usage is recorded when returned. Network/provider variability remains.
27. What does your checker fail to solve? Wrong retrieval, unencoded clinical rules, incorrect entered patient facts and hallucinated model explanations.
28. What if a drug is indicated but a field is missing? Identify the field and separate conditional planning from a patient-specific actionable instruction; retain other supported assessments/advice.
29. How would NER connect? Future NER would produce structured fields with negation/uncertainty, followed by human confirmation before entering the patient state.
30. How would doctor feedback connect? Store output/card/source IDs, accept/reject and reason. Curate changes offline instead of automatically changing medical rules.
31. How would prescription assembly connect? Only after doctor approval, complete drug fields and patient-specific safety checks. It is not implemented here.
32. What did AI help with? Code, source structuring, draft cases, documentation and paper discussion. You must personally review the evidence and explain your own edits/runs.
33. Why not claim the hypertension algorithm is done? It is a raster image not captured by plain text extraction. Preserving the image is not the same as verifying its branches.
34. What remains for the paper? Verify the final 2026 article's exact result/figure references. The current summary explicitly relies on the accessible preprint and author explanation.

## Live demo checklist
- Start the model service and Streamlit before the interview. Test the model connection.
- Use only fictional data. Keep exact PDFs open at relevant pages.
- Show patient input, retrieved cards, selected output and citations.
- Demonstrate C3 then C6, emphasizing only pregnancy changed.
- Enter an incomplete/new case; show clarifications rather than invented normal findings.
- Explain one failure honestly using the saved output and source.
- Know which parts are implemented, software-tested, model-tested, source-reviewed and clinically validated; these are different claims.

## Before submission
Read Q1_cards_and_reasoning.md and inspect each referenced page. Visually transcribe/review hypertension PDF page 64 if you want to claim its full implementation; ask for the correct chikungunya file/pages. Configure and run the actual model, freeze the final study, collect 12 real outputs and score them manually. Update the slides and comparison note using observed results. Never submit NOT_RUN as completed results.
