from openai import OpenAI
from rest_framework.exceptions import APIException

PROMPT_PATHS = ['/root/backend/aims/utils/prompt_txt/essay_prompt.txt', '/root/backend/aims/utils/prompt_txt/essay_prompt2.txt']

def summary_and_extract(api_key, content, criteria):
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )

    # Load the prompt and criteria
    try:
        with open(PROMPT_PATHS[0], 'r', encoding='utf-8') as f1, \
             open(PROMPT_PATHS[1], 'r', encoding='utf-8') as f2:
                prompt = f1.read()
                prompt2 = f2.read()
    except FileNotFoundError:
        raise APIException(f"Prompt file not found at path: {PROMPT_PATHS}")

    rule = criteria.get("평가 내용", "")

    # Chat API
    try:
        stream = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {
                    "role": "system",
                    "content": prompt + rule + prompt2
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

def first_evaluate(content, criteria):
    # 글자 수 계산
    char_cnt = len(content)
    
    # 글자 수 평가 기준 불러오기
    penalty = None
    for rule in criteria.get("분량", []):
        if rule["min"] <= char_cnt and char_cnt < rule["max"]:
            penalty = rule["penalty"]
            break
    
    evaluate = f"{char_cnt}자 : "
    if penalty == 0:
        evaluate += "감점 없음"
    elif penalty == None:
        evaluate += "분량 미충족"
    else:
        evaluate += f"{penalty}점 감점"

    return evaluate