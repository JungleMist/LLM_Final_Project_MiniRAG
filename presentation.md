# Presentation Outline: Mini-RAG for LLM Course Q&A

**Track C — Retrieval-Augmented Question Answering**
**Duration: ~8 minutes | ~10 slides**

---

## Slide 1 — Title

- **Title:** MiniRAG: Building and Evaluating a Retrieval-Augmented Q&A System for LLM Course Materials
- **Subtitle:** COM SCI-X 450.46 Final Project — Track C (Mini-RAG)
- Name, date

---

## Slide 2 — Problem & Motivation

**Problem:**
- LLMs have strong general knowledge but can hallucinate course-specific facts (deadlines, textbook titles, track names)
- A Q&A system for course materials needs answers *grounded in the actual documents*, not the model's parametric memory

**Why it matters:**
- Students regularly have questions about syllabus details, deliverables, and weekly topics
- A RAG system can answer these accurately if the right chunk is retrieved — without fine-tuning

**What we built:**
- An end-to-end RAG pipeline (MiniRAG) that indexes course PDFs and Markdown files, retrieves relevant chunks, and generates grounded answers
- Evaluated with RAGAS metrics across 11 ground-truth Q&A pairs, with a no-retrieval baseline for comparison

---

## Slide 3 — System Architecture

**Pipeline diagram (describe or draw):**

```
materials/ (PDFs, HTML, Markdown)
        ↓ chunker (400 tokens, 100 overlap)
        ↓ embedder (qwen3-embedding via NRP API)
        ↓ ChromaDB (persistent vector index)
                ↓
        _retrieve(query, k=3)   ← L2 nearest-neighbor search
                ↓
        retrieval.md prompt + gpt-oss (temp=0.3)
                ↓
        LLM Answer
                ↓
        RAGAS evaluation (faithfulness, context_precision,
                          answer_relevancy, answer_correctness)
```

**Key design decisions:**
- `force_initial=False` by default — SHA256 manifest detects only changed files, avoiding full re-indexing on every run
- RAGAS judge uses `temperature=0` and LangChain wrapper pointed at the same NRP endpoint for reproducible scoring
- No-RAG baseline: same LLM, same queries, but no retrieved context — isolates the retrieval contribution

---

## Slide 4 — Data & Setup

**Materials indexed:**

| Type | Files |
|------|-------|
| PDF | Syllabus, textbook (Hands-On LLMs) |
| HTML | Course landing page |
| Markdown | Week 1–8 overviews, Final Project docs |

**Evaluation dataset:**
- 11 hand-written ground-truth Q&A pairs (`dataset.json`)
- Cover: course logistics, weekly topics, RAG concepts, prompting strategies, optimization techniques, project requirements
- Each item: `query`, ground-truth `answer`, `llm_answer`, and RAGAS `evaluation` dict

**RAGAS metrics used:**

| Metric | Measures | Needs ground truth |
|--------|----------|:------------------:|
| `faithfulness` | Is the answer grounded in retrieved context? | No |
| `context_precision` | Did retrieval surface a relevant chunk? | Yes |
| `answer_relevancy` | Does the answer address the question? | No |
| `answer_correctness` | Does the answer match ground truth? | Yes |

---

## Slide 5 — Quantitative Results

**Average scores — RAG vs. No-RAG:**

| Metric | RAG | No-RAG | Δ |
|--------|:---:|:------:|:-:|
| `answer_relevancy` | 0.87 | 0.95 | −0.08 |
| `answer_correctness` | **0.45** | **0.40** | **+0.05** |
| `faithfulness` | 0.28 | — | — |
| `context_precision` | 0.36 | — | — |

- RAG improved `answer_correctness` on average, but the gain is modest
- The real split is *within* the RAG condition — by retrieval success

**Correctness split by retrieval quality:**

| Retrieval | Queries | Avg `answer_correctness` |
|-----------|:-------:|:------------------------:|
| Good (context_precision ≈ 1.0) | 4 of 11 | **0.68** |
| Poor (context_precision = 0.0) | 7 of 11 | **0.33** |

→ When retrieval works, the pipeline performs nearly twice as well

---

## Slide 6 — Per-Query Results Table

| ID | Query (short) | faith. | ctx_prec | ans_rel | ans_corr |
|----|--------------|:------:|:--------:|:-------:|:--------:|
| 1 | Required textbook | 0.00 | 0.00 | 0.98 | 0.22 |
| 2 | Four project tracks | 0.00 | 0.00 | 0.99 | 0.69 |
| 3 | Week 3 topics | 0.47 | 0.00 | 0.83 | 0.57 |
| 4 | RAG / Week 5 | 0.63 | **1.00** | 0.97 | 0.59 |
| 5 | Prompting strategies | 0.00 | 0.00 | 0.90 | 0.61 |
| 6 | Final project deliverables | 0.71 | 0.00 | **0.00** | 0.31 |
| 7 | Week 8 optimization | 0.38 | **1.00** | 0.93 | 0.54 |
| 8 | Evaluation frameworks | 0.81 | 0.00 | 0.89 | 0.24 |
| 9 | Python packages | 0.41 | 0.00 | 0.98 | 0.24 |
| 10 | Fine-tuning vs zero-shot | 0.62 | **1.00** | 0.97 | 0.58 |
| **11** | **Project proposal** | **1.00** | **1.00** | **0.99** | **0.87** |
| **Avg** | | 0.28 | 0.36 | 0.87 | 0.45 |

---

## Slide 7 — Demo: Success vs. Failure

### Success — Query 11 (proposal requirements)

> **Q:** What must the LLM course final project proposal include, and when was it due?

**Retrieved chunk:** Final_Project_Project_Proposal.md — a focused, self-contained document listing every required field.

**LLM answer (correct):** "Track & title, task description (3–5 sentences), planned models, data source & size, evaluation plan, backup plan. Due Monday May 18."

*faithfulness=1.00, context_precision=1.00, answer_correctness=0.87*

---

### Failure — Query 1 (required textbook)

> **Q:** What is the required textbook for COM SCI-X 450.46 Large Language Models?

**Retrieved chunk:** (irrelevant — did not contain syllabus ISBN or textbook entry)

**LLM answer (hallucination):** "The required textbook is *Deep Learning* by Ian Goodfellow, Yoshua Bengio, and Aaron Courville."

**Correct answer:** *Hands-On Large Language Models* by Jay Alammar & Maarten Grootendorst

*faithfulness=0.00, context_precision=0.00, answer_correctness=0.22*

---

### Notable — Query 6 (deliverables): LLM refusal

The model correctly admitted it could not find the deliverables in the retrieved context and gave a generic response. RAGAS scored `answer_relevancy=0.00` — the only case where this metric failed, because refusal counts as off-topic under RAGAS scoring.

---

## Slide 8 — Root Cause Analysis

**Why does retrieval fail on 7 of 11 queries?**

1. **Vocabulary mismatch for administrative content**
   - Queries like "required textbook" or "four project tracks" use terms that don't closely match prose in week-overview files
   - `qwen3-embedding` selects semantically adjacent but factually irrelevant chunks

2. **Chunk granularity**
   - 400-token overlapping chunks may include many topics, diluting the relevance signal
   - Administrative details buried mid-paragraph score poorly against surface-form queries

**Why `answer_relevancy` stays high (~0.87) even with bad retrieval?**
- The LLM always produces a topically on-target response using its parametric knowledge
- High relevancy ≠ high correctness — the scores measure different things and can diverge strongly

---

## Slide 9 — Lessons Learned

**1. Retrieval quality is the bottleneck, not the LLM**

Improving the prompt or switching models would not have fixed queries 1, 2, or 8. The LLM answered confidently with wrong information because the right chunk was never surfaced. The path to improvement is re-ranking, smaller chunk granularity, or hybrid (BM25 + dense) retrieval — not better generation.

**2. A high "relevancy" score can mask hallucination**

`answer_relevancy` measures whether the answer is topically on-target, not whether it is factually correct. In this system, it averaged 0.87 even for queries where the model fabricated course-specific facts. Relying on relevancy alone would give a false sense of system quality. `context_precision` and `answer_correctness` (which requires ground truth) are the more diagnostic metrics.

---

## Slide 10 — Conclusion & Next Steps

**Summary:**
- Built a working RAG pipeline (MiniRAG) with incremental indexing, dense retrieval, and RAGAS-based evaluation
- Compared RAG vs. no-RAG: RAG improves answer correctness when retrieval succeeds (0.68 vs 0.33)
- The system works well for focused, self-contained documents (project proposal, optimization week); it fails for administrative queries where vocabulary mismatches retrieval

**Priority improvements:**

| Priority | Action |
|----------|--------|
| High | Add a cross-encoder re-ranker after vector search to filter irrelevant chunks |
| High | Split administrative content into smaller, topic-focused chunks |
| Medium | Increase `k` (currently 3) to improve recall at the cost of precision |
| Medium | Add a retrieval confidence threshold — prompt the LLM to refuse consistently rather than hallucinate |
| Low | Hybrid BM25 + dense retrieval for keyword-heavy queries (ISBN, exact dates) |
