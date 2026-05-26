import asyncio
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import faithfulness, context_precision, answer_relevancy, answer_correctness, answer_similarity
from ragas.dataset_schema import SingleTurnSample

from config import MODEL, EMBEDDING_MODEL, NRP_TOK, NRP_URL

_llm = LangchainLLMWrapper(ChatOpenAI(
    model=MODEL, api_key=NRP_TOK, base_url=NRP_URL, temperature=0,
))
_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(
    model=EMBEDDING_MODEL, api_key=NRP_TOK, base_url=NRP_URL,
))

faithfulness.llm = _llm
context_precision.llm = _llm
answer_relevancy.llm = _llm
answer_relevancy.embeddings = _embeddings
answer_similarity.embeddings = _embeddings
answer_correctness.llm = _llm
answer_correctness.embeddings = _embeddings
answer_correctness.answer_similarity = answer_similarity

_METRICS = [faithfulness, context_precision, answer_relevancy, answer_correctness]


async def _score_all(sample):
    scores = await asyncio.gather(*[m.single_turn_ascore(sample) for m in _METRICS])
    return {m.name: score for m, score in zip(_METRICS, scores)}


def evaluation(query: str, contents: str | None, answer: str, reference: str) -> dict:

    sample = SingleTurnSample(
        user_input=query,
        retrieved_contexts=[contents],
        response=answer,
        reference=reference,
    )
    return asyncio.run(_score_all(sample))
