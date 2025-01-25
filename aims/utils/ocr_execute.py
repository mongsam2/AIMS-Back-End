# pip install requests

import requests
from ..models import Extraction
from rest_framework.response import Response


def execute_ocr(api_key, document_id, file):
    filename = file
    
    url = "https://api.upstage.ai/v1/document-ai/ocr"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    files = {"document": open(filename, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        content = [page.get("text", "") for page in response.json().get("pages", [])]
        Extraction.objects.create(content=content, document_id=document_id)

        return Response({'message': content})

    return Response({"message": "처리 실패"}, 400)