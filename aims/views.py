from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException

# 모델 (데이터베이스)
from aims.models import Extraction, Summarization, InappropriateReason, Evaluation 
from documents.models import Document
from rest_framework.exceptions import APIException

from aims.utils.summarization import txt_to_html, extract_pages_with_keywords, process_with_solar

from django.conf import settings
import requests
import os

from django.shortcuts import get_object_or_404
from aims.utils.essay import summary_and_extract, first_evaluate

from aims.utils.execute_ocr import execute_ocr
from aims.utils.execute_solar import get_answer_from_solar


API_KEY = os.environ.get('UPSTAGE_API_KEY')


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

        content = execute_ocr(API_KEY, file_path)
        Extraction.objects.create(content=content, document_id=document_id)

        return Response({'message': content})

    

class SummarizationView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        # LLM 길이 초과 문제 해결
                
            # 민솔이는  page_texts(ocr에서 Text 추출한 값) 이 값을 사용하면 됩니다 !
        
            # 추천면접질문 로직 추가 - 민솔
            
        '''
        html_content = txt_to_html(page_texts)
        pages_with_keywords = extract_pages_with_keywords(html_content)
        parse_response = parse_selected_pages(API_KEY, file_path, pages_with_keywords)
        solar_response = process_with_solar(API_KEY, parse_response)
        '''
        # TODO - from yejin : 이거 왜 ocr을 수행하는지? 파일이 업로드 되면 extraction에 ocr 결과가 저장됨 -> Extraction에서 content를 불러와서 쓰면 됨
        #extraction = execute_ocr(API_KEY, file_path)

        # Extraction을 가져와 solar로 prompting한 결과를 response에 저장
        extraction = Extraction.objects.get(id=document_id)

        prompt_file = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'student_record_prompt.txt')  
        
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
        
        response = get_answer_from_solar(API_KEY, extraction, prompt_content)

        # TODO - from yejin : 갑자기 document 왜 불러오는지?
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        Summarization.objects.create(content=response, document=document)

        return Response({
            'solar_response': response
            # 추천된 면접 질문 목록 추가 - 민솔
        })
    

class ReasonView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        return Response({'message': file_path})


class EvaluationView(APIView):
    def post(self, request, document_id):
        # TODO - from yejin : 주석이랑 코드랑 일치하지 않음
        # Extraction DB로부터 OCR 결과인 content를 갖고오기
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        content = document
        
        # 논술 OCR 내용인 content를 가지고 요약문 및 추출문 갖고오기
        # content의 글자 수 기반으로 1차 채점하기
        try:
            criteria = dict() # criteria 갖고 오기
            summary = summary_and_extract(API_KEY, content, criteria)
            evaluate = first_evaluate(content, criteria)
        except Exception as e:
            raise APIException(f"Error during summarization and evaluation: {str(e)}")

        rule = f'\n\n{criteria.get("평가 내용", "")}'
        Evaluation.objects.create(content=summary, document=document, memo=evaluate+rule)

        return Response({'message': 'Summarization successful', 'summary': summary, 'evaluate': evaluate+rule})
