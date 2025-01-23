from openai import OpenAI
from rest_framework.exceptions import APIException

PROMPT_PATH = './essay_prompt.txt'

def essay(api_key, content):
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    # Load the prompt
    try:
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except FileNotFoundError:
        raise APIException(f"Prompt file not found at path: {PROMPT_PATH}")

    # Chat API
    try:
        stream = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            stream=True,
            #temperature=0.2
        )
    except Exception as e:
        raise APIException(f"OpenAI API call failed: {str(e)}")

    summary_extract = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            summary_extract += chunk.choices[0].delta.content
    
    return summary_extract