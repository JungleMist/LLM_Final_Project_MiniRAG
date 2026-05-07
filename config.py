import os
import yaml
from pathlib import Path
from typing import Any, Tuple
from dotenv import load_dotenv
load_dotenv()

# DOCS
DOCS_PATH: str = "./materials"
ALLOWED_EXTS: Tuple = (".pdf", ".txt", ".md", ".html")
MANIFEST_PATH: str = "./manifest.json"

# Client
NRP_TOK: str = os.getenv("NRP_TOK")
NRP_CACHE_SALT: str = os.getenv("NRP_CACHE_SALT")
NRP_URL: str = "https://ellm.nrp-nautilus.io/v1"
MODEL: str = "gpt-oss"

# Judge LLM
JUDGE_SYS_PATH = "./prompts/judge_sys.md"
JUDGE_USER_PATH = "./prompts/judge_user.md"

# RAG
## Chromadb
CHROMADB_PATH: str = "./chroma"
DB_NAME: str = "docs"

## Chunk
CHUNK_SIZE: int = 800
CHUNK_OVERLAP: int = 200

## Embedding
HF_TOKEN: str = os.getenv("HF_TOKEN")
EMBEDDING_MODEL: str = "qwen3-embedding"

## Retrival
TOP_K: int = 3

## Prompt
PROMPT_PATH: str = "./prompts/retrieval.md"


if __name__ == "__main__":
    print(f"""
NRP_TOK: {NRP_TOK}
NRP_CACHE_SALT: {NRP_CACHE_SALT}
HF_TOKEN: {HF_TOKEN}
""")