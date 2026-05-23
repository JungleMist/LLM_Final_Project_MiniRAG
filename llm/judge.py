import asyncio
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import faithfulness, context_precision, answer_relevancy, answer_correctness, answer_similarity
from ragas.dataset_schema import SingleTurnSample

from config import NRP_TOK, NRP_URL, MODEL, EMBEDDING_MODEL

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


def evaluation(query: str, contents: str, answer: str, reference: str) -> dict:
    sample = SingleTurnSample(
        user_input=query,
        retrieved_contexts=[contents],
        response=answer,
        reference=reference,
    )
    return {
        m.name: asyncio.run(m.single_turn_ascore(sample))
        for m in _METRICS
    }
