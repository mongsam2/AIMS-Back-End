import os
import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException

from django.conf import settings
from django.shortcuts import get_object_or_404

# 모델 (데이터베이스)
from documents.models import Document, Documentation
from aims.models import Extraction, ExtractionEssay, Summarization, DocumentPassFail, Evaluation 

# utils 파일 불러오기
from django.conf import settings

from aims.utils.essay_evaluate import evaluate

from aims.utils.execute_apis import execute_ocr, get_answer_from_solar, parse_selected_pages
from aims.utils.summarization import txt_to_html, extract_pages_with_keywords, process_with_solar
from aims.utils.extract_sections import extract_sections, sections  

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
        extraction = Extraction.objects.get(document_id=document_id)
        content = extraction.content  
        
        extracted_texts = extract_sections(content, sections)

        summary_prompt_path = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'student_record_prompt.txt')
        interview_prompt_path = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'interview_questions.txt')
        
        with open(summary_prompt_path, 'r', encoding='utf-8') as f1,\
            open(interview_prompt_path, 'r', encoding='utf-8') as f2:
            summary_prompt = f1.read()
            interview_prompt = f2.read()
        
        summary = get_answer_from_solar(api_key, extracted_texts, summary_prompt)
        interview = get_answer_from_solar(api_key, extracted_texts, interview_prompt, 0., True)

        try:
            document = Documentation.objects.get(id=document_id)
        except Documentation.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        Summarization.objects.create(content=summary, document=document, question=interview)

        return Response({
            'summary': summary,
            'interview_questions' : interview
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
        
        extraction_essay = ExtractionEssay.objects.get(document_id=document_id)
        content = extraction_essay.content

        # OCR 인식률 저하 시 경고 메시지 저장
        if '경고: OCR 신뢰도가 낮습니다' in content:
            Evaluation.objects.create(content=content, document=document, memo=None)
            return Response({'message': 'Summarization failed', 'summary': content, 'evaluate': None})
        
        # 요약문 및 추출문 갖고오기
        # content의 글자 수 기반으로 1차 채점하기
        try:
            criteria = EssayCriteriaSerializer(document.criteria).data # criteria 갖고 오기
            summary_extract, penalty = evaluate(api_key, content, criteria)
        except Exception as e:
            raise APIException(f"Error during summarization and evaluation: {str(e)}")

        Evaluation.objects.create(content=summary_extract, document=document, memo=penalty)

        return Response({'message': 'Summarization successful', 'summary': summary_extract, 'evaluate': penalty})
