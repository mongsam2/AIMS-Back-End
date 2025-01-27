from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException


# 모델 (데이터베이스)
from aims.models import Extraction, Summarization, DocumentPassFail, Evaluation 
from documents.models import Document


from django.conf import settings
import requests
import os

from aims.utils.essay import summary_and_extract, first_evaluate
from aims.utils.essay_preprocess import preprocess_pdf

from aims.utils.execute_ocr import execute_ocr
from aims.utils.execute_solar import get_answer_from_solar


API_KEY = os.environ.get('UPSTAGE_API_KEY')

from django.core.files.temp import NamedTemporaryFile
from openai import OpenAI

# serializers
from aims.serializers import EssayCriteriaSerializer


# Create your views here.
def get_document_path(document_id):
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        raise NotFound('그 아이디는 없는 아이디요')
    return document.file_url.path


class ExtractionView(APIView):
    def post(self, request, document_id):
        file_path = get_document_path(document_id)
        
        content = execute_ocr(API_KEY, file_path)
        Extraction.objects.create(content=content, document_id=document_id)
        
        return Response({'message': content})
    

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
        
        response = get_answer_from_solar(API_KEY, extraction, prompt_content)

        # TODO - from yejin : 갑자기 document 왜 불러오는지?
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise NotFound(f"Document for document ID {document_id} is not found.")
        
        summarization_text = response

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
        
        # 논술 OCR 내용인 content를 가지고 오기 
        content = execute_ocr(API_KEY, document.file_url.path)[0]
        
        # 요약문 및 추출문 갖고오기
        # content의 글자 수 기반으로 1차 채점하기
        try:
            criteria = EssayCriteriaSerializer(document.criteria).data # criteria 갖고 오기
            print(criteria)
            summary = summary_and_extract(API_KEY, content, criteria)
            evaluate = first_evaluate(content, criteria)
        except Exception as e:
            raise APIException(f"Error during summarization and evaluation: {str(e)}")

        rule = f'\n\n{criteria.get("content", "")}'
        Evaluation.objects.create(content=summary, document=document, memo=evaluate+rule)

        return Response({'message': 'Summarization successful', 'summary': summary, 'evaluate': evaluate+rule})

