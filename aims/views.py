from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

# 모델 (데이터베이스)
from .models import Extraction, Summarization, InappropriateReason, Evaluation 
from documents.models import Document


from django.conf import settings
import os

# Create your views here.
def get_document_path(document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('그 아이디는 없는 아이디요')
    file_path = 'http://127.0.0.1:8000'+document.file_url.url
    return file_path

class ExtractionView(APIView):
    def post(self, request, document_id):
        document = Document.objects.get(id=document_id)
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})
    
class SummarizationView(APIView):
    def post(self, request, document_id):
        document = Document.objects.get(id=document_id)
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})

        return Response({'message': '딕셔너리 형태로 응답'})

class ReasonView(APIView):
    def post(self, request, document_id):
        document = Document.objects.get(id=document_id)
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})

        return Response({'message': '딕셔너리 형태로 응답'})

class EvaluationView(APIView):
    def post(self, request, document_id):
        document = Document.objects.get(id=document_id)
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})

        return Response({'message': '딕셔너리 형태로 응답'})