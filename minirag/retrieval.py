import torch
import chromadb
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .embedder import batch_embed
from .chunker import load_documents, chunk_documents
from .indexer import changed_files
from llm import client
from config import CHROMADB_PATH, DOCS_PATH, TOP_K, DB_NAME, PROMPT_PATH, ALLOWED_EXTS, MANIFEST_PATH


def _set_up_chromadb(docs_chunks: List[Dict], path: str = CHROMADB_PATH, name: str = DB_NAME):
    db_client = chromadb.PersistentClient(path=path)
    collection = db_client.get_or_create_collection(name=name)

    if not docs_chunks:
        print('nothing to update')
        return collection

    ids = [str(doc["id"]) for doc in docs_chunks]
    documents = [doc["text"] for doc in docs_chunks]
    metadatas = [doc["metadata"] for doc in docs_chunks]

    embeddings = batch_embed(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return collection


def _load_and_chunk(file_paths: List[Path]) -> List[Dict]:
    docs = load_documents(file_paths)
    docs_chunks = chunk_documents(docs)
    return docs_chunks


def _sim(texts: List[str], query: str) -> torch.Tensor:
    texts_embs = batch_embed(texts, convert_to_tensor=True)
    query_emb = batch_embed([query], convert_to_tensor=True)
    return query_emb @ texts_embs.T


class MiniRAG:
    def __init__(self,
                 docs_path: str = DOCS_PATH,
                 manifest_path: str = MANIFEST_PATH,
                 chromadb_path: str = CHROMADB_PATH,
                 db_name: str = DB_NAME,
                 force_initial=True):
        # Docs Load and Chunk
        docs_path = Path(docs_path)
        manifest_path = Path(manifest_path)

        if not docs_path.exists() or not docs_path.is_dir():
            raise NotADirectoryError(f"Folder not found or is not a directory: {docs_path}")

        if force_initial:
            self.file_paths = [
                p for p in docs_path.rglob("*")
                if p.is_file()
                   and p.suffix.lower() in ALLOWED_EXTS
                   and not any(i.startswith('.') for i in p.parts)
            ]
            print('Initial all files:', [str(p) for p in self.file_paths])
        else:
            self.file_paths = changed_files(docs_path, manifest_path)
            print('Update changed files:', [str(p) for p in self.file_paths])
        self.docs_chunks = _load_and_chunk(self.file_paths)

        # Chromadb set up
        self.collection = _set_up_chromadb(self.docs_chunks,
                                           path=chromadb_path,
                                           name=db_name)

    def _retrieve(self, query: str, k: int = TOP_K) -> List[Dict]:
        q_emb = batch_embed([query])

        result = self.collection.query(
            query_embeddings=q_emb,
            n_results=k,
        )

        docs = result["documents"][0]
        metas = result["metadatas"][0]
        dists = result["distances"][0]

        hits = []
        for text, meta, dist in zip(docs, metas, dists):
            hits.append({
                "score": float(dist),
                "text": text,
                "metadata": meta,
            })
        return hits

    def response(self, query):
        hits = self._retrieve(query)
        contents = ""
        for hit in hits:
            contents += hit['text'] + "\n\n"

        with open(PROMPT_PATH, 'r') as f:
            sys_prompt = f.read().replace("{contents}", contents)

        return contents, client.output(sys_prompt, query)



if __name__ == "__main__":
    pass
