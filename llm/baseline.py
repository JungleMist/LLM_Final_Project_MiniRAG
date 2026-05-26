from llm.client import output

_SYS_PROMPT = (
    "You are a helpful assistant for the COM SCI-X 450.46 Large Language Models course. "
    "Answer the question concisely and accurately based on your knowledge."
)


def answer_without_rag(query: str) -> str:
    return output(_SYS_PROMPT, query)
