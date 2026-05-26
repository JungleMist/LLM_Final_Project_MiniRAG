import time
from pathlib import Path
import pytest

from llm.judge import evaluation
from minirag import embedder, chunker
from minirag.retrieval import MiniRAG
from config import DOCS_PATH

def test_rag_embedder():
    texts = [
        "I love machine learning.",
        "Neural networks are fascinating.",
        "The cat sat on the mat.",
    ]
    results = embedder.batch_embed(texts)
    assert(type(results) == list and type(results[0] == list))
    # print(type(results[0]))
    # print([len(result) for result in results])

def test_rag_chunker():
    raw_docs = chunker.load_documents([Path(DOCS_PATH) / 'LLM_Syllabus.pdf'])
    chunks = chunker.chunk_documents(raw_docs, chunk_size=1000, chunk_overlap=200)

    print(len(chunks), "chunks")
    print(chunks[0]["metadata"], chunks[-1]["text"][:200], "...")

def test_rag_retrieve():
    rag = MiniRAG()
    query = "What's the grading criteria for this class?"
    hits = rag._retrieve(query)
    for h in hits:
        print(h["score"], h["metadata"], h["text"][:80], "...")

def test_rag_response():
    rag = MiniRAG()
    query = "What's the grading criteria for this class?"
    contents, answer = rag.response(query)
    print(contents)
    print(answer)

def test_judge():
    rag = MiniRAG()
    query = "What's the grading criteria for this class?"
    reference = "Quizzes 5%, Discussion Points 10%, Assignments 60% and Final Project 25%."
    contents, answer = rag.response(query)
    start = time.time()
    comment = evaluation(query, contents, answer, reference)
    print("time: ", time.time()-start)
    print(comment)

