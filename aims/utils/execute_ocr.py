# pip install requests

import requests


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

    return "처리 실패"