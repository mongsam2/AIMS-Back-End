import os

from django.conf import settings
from rest_framework.exceptions import APIException

from aims.tasks import get_answer_from_solar


PROMPT_PATHS = [
    os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'essay_prompt.txt'),
    os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'essay_prompt2.txt')
]


def evaluate(api_key, content, criteria):
    # prompt 불러오기
    try:
        with open(PROMPT_PATHS[0], 'r', encoding='utf-8') as f1, \
             open(PROMPT_PATHS[1], 'r', encoding='utf-8') as f2:
                prompt = f1.read()
                prompt2 = f2.read()
    except FileNotFoundError:
        raise APIException(f"Prompt file not found at path: {PROMPT_PATHS}")

    rule = criteria.get("content", "")
    summary_extract = get_answer_from_solar(api_key, content, f"{prompt}\n{rule}\n{prompt2}")
    
    # 글자 수 계산
    char_cnt = len(content)
    
    # 글자 수 평가 기준 불러오기
    penalty = None
    for rule in criteria.get("ranges", []):
        if rule["min_value"] <= char_cnt and char_cnt < rule["max_value"]:
            penalty = rule["penalty"]
            break

    return summary_extract, penalty