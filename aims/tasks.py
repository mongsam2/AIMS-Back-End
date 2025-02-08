# pip install requests
# pip install openai

import requests
from openai import OpenAI # openai==1.52.2
from celery import shared_task


@shared_task
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
        confidence = response.json().get("confidence", 0)
        return content[0], confidence
    
    print(f"Request failed with status code: {response.status_code}")
    print(f"Response content: {response.text}")

    return "처리 실패", 0.


@shared_task
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
        

@shared_task
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


@shared_task
def execute_embedding(queries, api_key):

    """
    1개 이상 100개 미만의 토큰에 대한 임베딩을 일괄 처리
    각 텍스트에 대한 토큰은 4,000 미만이어야 하고
    리스트 전체의 토큰 수는 204,800보다 작아야 한다

    Args:
        queries(list): 리스트 형태의 text
        api_key(str): 업스테이지 API 키

    Returns:
        embedding(list): 리스트 형태의 embedding 결과
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1/solar"
    )
    
    query_embedding = client.embeddings.create(
        model = "embedding-passage",
        input = queries
    ).data

    embedding_list = [i.embedding for i in query_embedding]

    return embedding_list