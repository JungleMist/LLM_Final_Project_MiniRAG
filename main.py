from minirag.retrieval import MiniRAG
from llm.judge import evaluation
import json


def main():
    with open("dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    rag = MiniRAG(force_initial=False)

    results = []
    for item in dataset["data"]:
        query = item["query"]
        reference = item["answer"]
        contents, llm_answer = rag.response(query)
        eval_dict = evaluation(query, contents, llm_answer, reference)

        results.append({
            "id": item["id"],
            "query": query,
            "answer": reference,
            "llm_answer": llm_answer,
            "evaluation": eval_dict,
        })
        print(f"[{item['id']}] done — faithfulness={eval_dict.get('faithfulness'):.2f}, "
              f"correctness={eval_dict.get('answer_correctness'):.2f}")

    output = {"data": results}
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} results to output.json")


if __name__ == "__main__":
    main()
