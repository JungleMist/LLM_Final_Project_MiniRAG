import torch
from openai import OpenAI
from typing import List, Optional
from config import EMBEDDING_MODEL, NRP_TOK

client = OpenAI(api_key = NRP_TOK,
                base_url = "https://ellm.nrp-nautilus.io/v1")

def _embed(text: str) -> List[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding

def batch_embed(texts: List[str], convert_to_tensor=False) -> torch.Tensor | List[List[float]]:
    vectors = [_embed(t) for t in texts]
    return torch.tensor(vectors) if convert_to_tensor else vectors


if __name__ == "__main__":
    texts = [
        "I love machine learning.",
        "Neural networks are fascinating.",
        "The cat sat on the mat.",
    ]
    results = batch_embed(texts, convert_to_tensor=True)
    print(results.shape)

