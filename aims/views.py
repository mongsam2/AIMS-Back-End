from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

# 모델 (데이터베이스)
from .models import Document, Extraction, Summarization, InappropriateReason, Evaluation

import os
import requests
from openai import OpenAI
from django.conf import settings
from tempfile import NamedTemporaryFile

from django.shortcuts import get_object_or_404

from .utils.essay import summary_and_extract, first_evaluate
from .utils.essay_preprocess import preprocess_pdf

from .utils.summarization import txt_to_html, extract_pages_with_keywords, parse_selected_pages, process_with_solar


# Create your views here.
def get_document_path_and_type(document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('그 아이디는 없는 아이디요')
    #file_path = 'http://127.0.0.1:8000'+document.file_url.url
    return document.file_url.path, document.document_type

def extract_text(document_id):
    file_path, doc_type = get_document_path_and_type(document_id)
    url = "https://api.upstage.ai/v1/document-ai/ocr"
    headers = {"Authorization": f"Bearer {api_key}"}

    # 논술일 때만 데이터 전처리
    if doc_type == "논술":
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            preprocess_pdf(file_path, temp_path)
            file_path = temp_path
    
    try:
        # Upstage API
        with open(file_path, "rb") as file:
            files = {"document": file}
            response = requests.post(url, headers=headers, files=files)
            if response.status_code == 200:
                content = response.json().get('text', '')
                Extraction.objects.create(content=content, document_id=document_id)
                
                return content
    except Exception as e:
        
        return Response({"message": f"처리 실패: {str(e)}"}, 400)
    finally:
        if doc_type == "논술" and os.path.exists(file_path):
            os.remove(file_path)
    
    return Response({"message": "처리 실패"}, 400)

api_key = os.environ.get('UPSTAGE_API_KEY')

class ExtractionView(APIView):
    def post(self, request, document_id):
        file_path, doc_type = get_document_path_and_type(document_id)
        url = "https://api.upstage.ai/v1/document-ai/ocr"
        headers = {"Authorization": f"Bearer {api_key}"}

        if doc_type == "논술":
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_path = temp_file.name
                preprocess_pdf(file_path, temp_path)
                file_path = temp_path
        
        try:
            # Upstage API
            with open(file_path, "rb") as file:
                files = {"document": file}
                response = requests.post(url, headers=headers, files=files)
                if response.status_code == 200:
                    content = response.json().get('text', '')
                    Extraction.objects.create(content=content, document_id=document_id)
                    
                    return Response({'message': content})
        except Exception as e:
            
            return Response({"message": f"처리 실패: {str(e)}"}, 400)
        finally:
            if doc_type == "논술" and os.path.exists(file_path):
                os.remove(file_path)
        
        return Response({"message": "처리 실패"}, 400)
    
class SummarizationView(APIView):
    def post(self, request, document_id):
        extraction = extract_text(document_id)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.upstage.ai/v1/solar"
        )
        prompt_file = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'student_record_prompt.txt')  
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
        parse_text = extraction
        stream = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {
                    "role": "system",
                    "content": prompt_content
                },
                {
                    "role": "user",
                    "content": parse_text
                }
            ],
            stream=False,
        )
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        summarization_text = stream.choices[0].message.content 

        # 면접 질문 생성
        prompt_file = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'interview_questions.txt')  
        with open(prompt_file, 'r', encoding='utf-8') as file:
            prompt_content = file.read()
        
        # 면접 질문 생성 chat api
        stream = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {
                    "role": "user",
                    "content": extraction + "\n---\n" + prompt_content
                }
            ],
            stream=True,
        )

        # 생성된 면접 질문 -> questions에 저장
        questions = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                questions += chunk.choices[0].delta.content
        
        Summarization.objects.create(content=summarization_text, document=document, question=questions)
        return Response({
            'summarization': summarization_text,
            'questions': questions
        })
    
class ReasonView(APIView):
    def post(self, request, document_id):
        file_path, doc_type = get_document_path_and_type(document_id)
        
        return Response({'message': file_path})

class EvaluationView(APIView):
    def post(self, request, document_id):
        # Extraction DB로부터 OCR 결과인 content를 갖고오기
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        extraction = extract_text(document_id)
        content = str(extraction)
        
        # 논술 OCR 내용인 content를 가지고 요약문 및 추출문 갖고오기
        # content의 글자 수 기반으로 1차 채점하기
        try:
            criteria = dict() # criteria 갖고 오기
            summary = summary_and_extract(api_key, content, criteria)
            evaluate = first_evaluate(content, criteria)
        except Exception as e:
            raise APIException(f"Error during summarization and evaluation: {str(e)}")

        rule = f'\n\n{criteria.get("평가 내용", "")}'
        Evaluation.objects.create(content=summary, document=document, memo=evaluate+rule)

        return Response({'message': 'Summarization successful', 'summary': summary, 'evaluate': evaluate+rule})

