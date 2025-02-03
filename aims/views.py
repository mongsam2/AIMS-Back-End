import os
import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException

from django.conf import settings
from django.shortcuts import get_object_or_404

# 모델 (데이터베이스)
from documents.models import Document
from aims.models import Extraction, ExtractionEssay, Summarization, DocumentPassFail, Evaluation 

# utils 파일 불러오기
from django.conf import settings

from aims.utils.essay_evaluate import evaluate

from aims.utils.execute_apis import execute_ocr, get_answer_from_solar, parse_selected_pages
from aims.utils.summarization import txt_to_html, extract_pages_with_keywords, process_with_solar

# serializers
from aims.serializers import EssayCriteriaSerializer

api_key = settings.API_KEY

def get_document_path(document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('그 아이디는 없는 아이디요')
    #file_path = 'http://127.0.0.1:8000'+document.file_url.url
    return document.file_url.path


class ExtractionView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        content = execute_ocr(api_key, file_path)
        Extraction.objects.create(content=content, document=document_id)

        return Response({'message': content})

class SummarizationView(APIView):
    def post(self, request, document_id):

        # Extraction을 가져와 solar로 prompting한 결과를 response에 저장
        extraction = Extraction.objects.get(id=document_id)

        prompt_file = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'student_record_prompt.txt')  
        
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
        
        response = get_answer_from_solar(api_key, extraction, prompt_content)

        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        Summarization.objects.create(content=response, document=document)

        return Response({
            'solar_response': response
            # 추천된 면접 질문 목록 추가 - 민솔
        })
    

class DocumentPassFailView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})


class EvaluationView(APIView):
    def post(self, request, document_id):
        # Document 객체 갖고오기
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        extraction_essay = ExtractionEssay.objects.get(id=document_id)
        content = extraction_essay.content

        # 요약문 및 추출문 갖고오기
        # content의 글자 수 기반으로 1차 채점하기
        try:
            criteria = EssayCriteriaSerializer(document.criteria).data # criteria 갖고 오기
            summary_extract, penalty = evaluate(api_key, content, criteria)
        except Exception as e:
            raise APIException(f"Error during summarization and evaluation: {str(e)}")

        Evaluation.objects.create(content=summary_extract, document=document, memo=penalty)

        return Response({'message': 'Summarization successful', 'summary': summary_extract, 'evaluate': penalty})
