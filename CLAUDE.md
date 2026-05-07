# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- Python environment: conda env named `llm` (configured in PyCharm)
- Run Python via: `conda run -n llm python <script>`
- API endpoint: `https://ellm.nrp-nautilus.io/v1` (OpenAI-compatible, not standard OpenAI)
- Credentials stored in `.env` (`NRP_TOK`, `NRP_CACHE_SALT`, `HF_TOKEN`)

## Commands

```bash
# Run test/dev script (primary entry point for development)
conda run -n llm python test.py

# Run individual module smoke tests (each has a __main__ block)
conda run -n llm python minirag/chunker.py
conda run -n llm python minirag/embedder.py
conda run -n llm python minirag/retrieval.py
conda run -n llm python llm/client.py
conda run -n llm python config.py   # prints env vars to verify .env is loaded
```

Note: `main.py` is currently broken (imports non-existent `rag` module). Use `test.py` instead.

## Architecture

This is a RAG + LLM-judge pipeline for querying LLM course materials.

**Primary query flow:**
```
materials/ (PDF, HTML) → chunker → embedder (qwen3-embedding) → ChromaDB
                                                                      ↓
                                                            MiniRAG._retrieve(query)
                                                                      ↓
                                                            prompts/retrieval.md + llm/client.output()
                                                                      ↓
                                                            llm/judge.evaluation()  ← prompts/judge_*.md
```

**Key modules:**
- `minirag/chunker.py` — Loads PDF/HTML/TXT/MD files, splits into overlapping text chunks with metadata
- `minirag/embedder.py` — Calls NRP API for `qwen3-embedding` embeddings; returns list or PyTorch tensor
- `minirag/indexer.py` — SHA256-based file change detection against `manifest.json` for incremental re-indexing
- `minirag/retrieval.py` — `MiniRAG` class: on init indexes docs into ChromaDB, then exposes `_retrieve(query, k)` and `response(query)` (returns `(contents_str, answer_str)`)
- `llm/client.py` — `output(sys_prompt, user_text)` wrapper for OpenAI-compatible chat completions (`gpt-oss` model)
- `llm/judge.py` — `evaluation(query, contents, answer)` calls the same LLM with judge prompts to score/comment on RAG answers
- `config.py` — Loads `.env` and exposes all constants; **this is the true source of configuration** (values are hardcoded here, not read from `config.yaml`)
- `prompts/retrieval.md` — System prompt for RAG answers; `{contents}` is filled with retrieved chunks
- `prompts/judge_sys.md` / `prompts/judge_user.md` — Judge LLM prompts; user template uses `{query}`, `{contents}`, `{answer}`

**`MiniRAG` initialization modes:**
- `MiniRAG(force_initial=True)` — re-indexes all files in `materials/` (default)
- `MiniRAG(force_initial=False)` — only indexes files changed since last run (uses `manifest.json`)

**ChromaDB persistence:** Vector index stored in `./chroma/`. Delete to force full re-indexing.

**`config.yaml` vs `config.py`:** `config.yaml` lists the intended parameters but `config.py` does not read from it — the constants in `config.py` are hardcoded. If you change a value, update `config.py` directly.

## Dependencies

```
openai
torch
chromadb
pypdf
beautifulsoup4
python-dotenv
pyyaml
```
