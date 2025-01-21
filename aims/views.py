from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

# 모델 (데이터베이스)
from .models import Extraction, Summarization, InappropriateReason, Evaluation 
from documents.models import Document


from django.conf import settings
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Create your views here.
def get_document_path(document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('그 아이디는 없는 아이디요')
    #file_path = 'http://127.0.0.1:8000'+document.file_url.url
    return document.file_url.path

api_key = os.environ.get('UPSTAGE_API_KEY')

class ExtractionView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        url = "https://api.upstage.ai/v1/document-ai/ocr"
        headers = {"Authorization": f"Bearer {api_key}"}

        # upstage api
        with open(file_path, "rb") as file:
            files = {"document": file}
            response = requests.post(url, headers=headers, files=files).json()
        
        Extraction.objects.create(content=response.get("text"), document_id=document_id)
        
        return Response({'message': '성공적으로 추출되었습니다.'})
    
class SummarizationView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})

class ReasonView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})

class EvaluationView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})