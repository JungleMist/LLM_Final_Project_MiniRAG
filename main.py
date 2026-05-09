from minirag.retrieval import MiniRAG
from llm.judge import evaluation
import json
import re


def _parse_eval(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError(f"Cannot parse JSON from judge output: {text!r}")


def main():
    with open("dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    rag = MiniRAG(force_initial=True)

    results = []
    for item in dataset["data"]:
        query = item["query"]
        contents, llm_answer = rag.response(query)
        eval_dict = _parse_eval(evaluation(query, contents, llm_answer))

        results.append({
            "id": item["id"],
            "query": query,
            "answer": item["answer"],
            "llm_answer": llm_answer,
            "evaluation": eval_dict,
        })
        print(f"[{item['id']}] done — relevance={eval_dict.get('content relevance score')}, "
              f"coherence={eval_dict.get('answer coherence score')}")

    output = {"data": results}
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} results to output.json")


if __name__ == "__main__":
    main()
