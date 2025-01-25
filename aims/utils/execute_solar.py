# pip install openai

from openai import OpenAI # openai==1.52.2

def get_answer_from_solar(api_key, content, prompt, temperature=0.7):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    response = client.chat.completions.create(
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
        stream=False,
        temperature=temperature
    )

    return response.choices[0].message.content