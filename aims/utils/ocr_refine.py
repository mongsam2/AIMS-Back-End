# pip install openai

from openai import OpenAI # openai==1.52.2

def refine_ocr_with_solar(api_key, content, prompt, temperature=0.7, ):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

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
        temperature=temperature
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    
    # Use with stream=False
    # print(stream.choices[0].message.content)