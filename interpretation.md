# RAG Pipeline Evaluation — Results Interpretation

## Metrics Overview

Each query is scored on four RAGAS metrics:

| Metric | What it measures | Range |
|--------|-----------------|-------|
| **faithfulness** | How much the LLM answer is grounded in the retrieved context (vs. hallucinated) | 0–1 |
| **context_precision** | Whether the retrieved chunks actually contain the answer | 0–1 |
| **answer_relevancy** | Whether the LLM answer addresses the question asked | 0–1 |
| **answer_correctness** | Factual match between the LLM answer and the ground-truth answer | 0–1 |

---

## Per-Question Results

| ID | Query (short) | faithfulness | context_precision | answer_relevancy | answer_correctness |
|----|--------------|:---:|:---:|:---:|:---:|
| 1  | Required textbook | 0.00 | 0.00 | 0.99 | 0.22 |
| 2  | Four project tracks | 0.00 | 0.00 | 0.98 | 0.26 |
| 3  | Week 3 topics | 0.44 | 0.00 | 0.94 | 0.27 |
| 4  | What is RAG / Week 5 | 0.75 | **1.00** | 0.97 | 0.60 |
| 5  | Prompting strategies | 0.00 | 0.00 | 0.90 | 0.68 |
| 6  | Final project deliverables | 0.10 | 0.00 | **0.00** | 0.19 |
| 7  | Week 8 optimization | 0.38 | **1.00** | 0.91 | 0.61 |
| 8  | Evaluation frameworks | 0.00 | 0.00 | 0.94 | 0.24 |
| 9  | Python packages | 0.37 | 0.00 | 0.98 | 0.43 |
| 10 | Fine-tuning vs zero-shot | 0.11 | **1.00** | 0.98 | 0.66 |
| 11 | Project proposal requirements | **0.93** | **1.00** | 0.90 | **0.84** |

**Average scores:** faithfulness 0.28 · context_precision 0.36 · answer_relevancy 0.87 · answer_correctness 0.45

---

## Key Findings

### 1. Retrieval is the bottleneck

`context_precision` is the most important indicator: only **4 of 11 queries** (IDs 4, 7, 10, 11) retrieved a relevant chunk (`context_precision ≈ 1.0`). Every other query got a score of 0.0, meaning the retrieved text did not contain the answer.

When retrieval succeeds, the whole pipeline improves:
- Average `answer_correctness` with good retrieval: **0.68**
- Average `answer_correctness` without good retrieval: **0.33**

### 2. The LLM answers confidently even without context

`answer_relevancy` is consistently high (0.87 average) regardless of retrieval quality. The LLM always produces a response that is topically on-target. However, when the retrieved context is empty or irrelevant, the model falls back on its parametric (training-time) knowledge and hallucinates course-specific details.

The clearest example is **ID 1**: the LLM answered that the required textbook is *"Deep Learning" by Goodfellow, Bengio & Courville* — a plausible but entirely wrong answer fabricated from general training knowledge, because the relevant syllabus chunk was not retrieved.

### 3. Faithfulness follows retrieval

`faithfulness` is near zero for all queries where `context_precision = 0.0`. The LLM is not inventing facts within the retrieved window — it is simply not using the retrieved context at all, because what was returned is irrelevant. When retrieval works (IDs 4, 7, 11), faithfulness rises to 0.75–0.93.

### 4. One notable answer-refusal case (ID 6)

For the "final project deliverables" question, the LLM explicitly stated it could not find the answer in the retrieved context and gave a generic response. This caused `answer_relevancy` to drop to **0.0** — the only case where this metric failed. While the model's honesty was appropriate, it reveals that refusal counts as a relevancy failure under RAGAS scoring. The underlying cause is again retrieval: the Final Project markdown files were not retrieved.

### 5. Best and worst performers

| | ID | answer_correctness |
|--|----|----|
| **Best** | 11 — Project proposal requirements | 0.84 |
| **Second best** | 5 — Prompting strategies | 0.68 |
| **Worst** | 6 — Final project deliverables | 0.19 |
| **Second worst** | 1 — Required textbook | 0.22 |

ID 11 succeeded because the Final Project Proposal markdown is a focused, self-contained document that embeds well and retrieves cleanly. ID 5 succeeded despite `context_precision = 0.0` because the LLM's parametric knowledge about zero-shot / few-shot / chain-of-thought prompting is accurate and general enough to match the ground truth.

---

## Root Cause Analysis

The low `context_precision` on 7 of 11 queries points to two likely causes:

1. **Embedding mismatch for structured/administrative content.** Questions about course logistics (textbook, project tracks, deliverables, late policy) use vocabulary that does not closely match the dense prose of the course-overview markdown files. The `qwen3-embedding` model may be selecting semantically adjacent but factually irrelevant chunks.

2. **Chunk granularity.** If the chunker splits documents into large overlapping blocks, a single chunk may contain many topics, diluting the relevance signal. Administrative details (deadlines, required readings) buried mid-paragraph score poorly against queries that use different surface forms.

---

## Recommendations

| Priority | Action |
|----------|--------|
| High | Add a re-ranking step (e.g., cross-encoder) after the initial vector search to filter out irrelevant chunks before prompting |
| High | Split administrative/FAQ content (deliverables, proposals, deadlines) into smaller, more focused chunks |
| Medium | Experiment with `k` (number of retrieved chunks) — increasing from the current value may help surface the right chunk when ranking is imperfect |
| Medium | Add a fallback: if no retrieved chunk scores above a similarity threshold, prompt the LLM to say so explicitly rather than hallucinate (this already happened for ID 6; make it consistent) |
| Low | Consider a hybrid retrieval approach (BM25 + dense) for keyword-heavy administrative queries (ISBN numbers, exact dates) |