from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

# 모델 (데이터베이스)
from .models import Extraction, Summarization, InappropriateReason, Evaluation 
from documents.models import Document
from rest_framework.exceptions import APIException

from .utils.summarization import txt_to_html, extract_pages_with_keywords, parse_selected_pages, process_with_solar
from .utils.essay import essay

from django.conf import settings
import requests
import os

from django.shortcuts import get_object_or_404

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

         # OCR API 호출
        url = "https://api.upstage.ai/v1/document-ai/ocr"
        headers = {"Authorization": f"Bearer {api_key}"}

        

        with open(file_path, "rb") as file:
            files = {"document": file}
            response = requests.post(url, headers=headers, files=files)
            
            if response.status_code == 200:
                output_data = response.json()
                pages = output_data.get("pages", [])
                page_texts = [page.get("text", "") for page in pages]
                
               # 민솔이는  page_texts(ocr에서 Text 추출한 값) 이 값을 사용하면 됩니다 !
               
               # 추천면접질문 로직 추가 - 민솔
               
                html_content = txt_to_html(page_texts)
                pages_with_keywords = extract_pages_with_keywords(html_content)
                parse_response = parse_selected_pages(file_path, pages_with_keywords)
                solar_response = process_with_solar(parse_response)
                document = get_object_or_404(Document, id=document_id)
                Summarization.objects.create(content=solar_response, document=document)
                return Response({
                    'solar_response': solar_response
                    # 추천된 면접 질문 목록 추가 - 민솔
                })
            else:
                return Response({'error': 'OCR 처리 실패'}, status=response.status_code)

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
            raise NotFound(f"해당 id의 document가 없습니다")
        
        try:
            extraction = Extraction.objects.get(document=document)
            content = extraction.content
        except Extraction.DoesNotExist:
            raise NotFound(f"extraction 가져오기 실패")
        
        # 논술 OCR 내용인 content를 가지고 요약문 및 추출문 갖고오기
        try:
            summary = essay(api_key, content)
        except Exception as e:
            raise APIException(f"Error during summarization: {str(e)}")
        
        Evaluation.objects.create(content=summary, document=document)
        return Response({'message': 'Summarization successful', 'summary': summary})