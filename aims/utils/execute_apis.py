# pip install requests
# pip install openai

import requests
from openai import OpenAI # openai==1.52.2
from celery import shared_task


def execute_ocr(api_key, file_path):
    
    """
    Args:
        api_key (str): UPSTAGE API KEY
        file_path (str): django 데이터베이스에서 파일

    Returns:
        text: ocr에서 추출한 멀티라인 문자열 반환
    """

    filename = file_path
    
    url = "https://api.upstage.ai/v1/document-ai/ocr"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    files = {"document": open(filename, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        content = [page.get("text", "") for page in response.json().get("pages", [])]
        return content
    
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response content: {response.text}")

    return "처리 실패"


def parse_selected_pages(api_key, file_path, pages):
    url = "https://api.upstage.ai/v1/document-ai/document-parse"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    page_numbers = ','.join(map(str, pages))
    data = {"ocr": "force", "base64_encoding": '["table"]', "pages": page_numbers}
    
    with open(file_path, "rb") as file:
        files = {"document": file}
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'PDF 파싱 실패', 'status_code': response.status_code}
        

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