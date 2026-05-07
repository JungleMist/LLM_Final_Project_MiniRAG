from openai import OpenAI

from config import NRP_TOK, NRP_CACHE_SALT, MODEL, NRP_URL


def output(system: str, user: str) -> str:
    """
    Base API calling

    :param text: LLM input
    :return: LLM output
    """
    client = OpenAI(api_key=NRP_TOK,
                    base_url=NRP_URL)

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{'role': 'system',
                   'content': system},
                    {'role': 'user',
                   'content': user}],
        extra_body={
            "cache_salt": NRP_CACHE_SALT
        },
        temperature=0.3
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    print(output("hello"))
