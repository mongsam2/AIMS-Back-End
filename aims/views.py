from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException

# 모델 (데이터베이스)
from .models import Extraction, Summarization, InappropriateReason, Evaluation 
from documents.models import Document


from django.conf import settings
import requests
from dotenv import load_dotenv
import os
load_dotenv()

from .utils.essay import essay

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
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                content = response.json()['text']
                Extraction.objects.create(content=content, document_id=document_id)
                return Response({'message': content})
        return Response({"message": "처리 실패"}, 400)
    
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
        # Extraction DB로부터 OCR 결과인 content를 갖고오기
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        try:
            extraction = Extraction.objects.get(document=document)
            content = extraction.content
        except Extraction.DoesNotExist:
            raise NotFound(f"Extraction record for Document is not found.")
        
        # 논술 OCR 내용인 content를 가지고 요약문 및 추출문 갖고오기
        try:
            summary = essay(api_key, content)
        except Exception as e:
            raise APIException(f"Error during summarization: {str(e)}")

        Evaluation.objects.create(content=summary, document=document)

        return Response({'message': 'Summarization successful', 'summary': summary})