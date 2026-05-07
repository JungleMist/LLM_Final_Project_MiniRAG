from openai import OpenAI

from config import NRP_TOK, NRP_URL, MODEL, JUDGE_SYS_PATH, JUDGE_USER_PATH, NRP_CACHE_SALT


def evaluation(
        query: str,
        contents: str,
        answer: str
) -> str:
    """
    Judgement LLM that provide evaluation comments
    """

    with open(JUDGE_SYS_PATH, 'r') as f:
        sys_prompt = f.read()
    with open(JUDGE_USER_PATH, 'r') as f:
        user_prompt = f.read().replace("{query}", query).replace("{contents}", contents).replace("{answer}", answer)

    client = OpenAI(api_key=NRP_TOK,
                    base_url=NRP_URL)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{'role': 'system',
                   'content': sys_prompt},
                  {'role': 'user',
                   'content': user_prompt}],
        extra_body={
            "cache_salt": NRP_CACHE_SALT
        },
        temperature=0 # be objective
    )

    return completion.choices[0].message.content