import json
from llm.baseline import answer_without_rag
from llm.judge import evaluation_no_rag


def main():
    with open("dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = []
    for item in dataset["data"]:
        query = item["query"]
        reference = item["answer"]
        llm_answer = answer_without_rag(query)
        eval_dict = evaluation_no_rag(query, llm_answer, reference)

        results.append({
            "id": item["id"],
            "query": query,
            "answer": reference,
            "llm_answer": llm_answer,
            "evaluation": eval_dict,
        })
        print(f"[{item['id']}] done — "
              f"relevancy={eval_dict.get('answer_relevancy'):.2f}, "
              f"correctness={eval_dict.get('answer_correctness'):.2f}")

    output = {"data": results}
    with open("output_no_rag.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} results to output_no_rag.json")


if __name__ == "__main__":
    main()