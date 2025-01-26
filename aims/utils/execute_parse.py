import json
import requests


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