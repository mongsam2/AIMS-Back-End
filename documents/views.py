from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Document, Documentation
from aims.models import Summarization, Evaluation

from .serializers import DocumentSerializer, DocumentReasonsSerializer, DocumentStatusSerializer, RawDataSerializer, DocumentationSerializer
from aims.serializers import EvaluationSerializer, SummarizationSerializer, EssayCriteriaSerializer

from django.core.exceptions import ValidationError
from django.conf import settings

from .tasks import process_ocr_task, process_ocr_task_for_essay, process_inference
from .utils.essay_preprocess import preprocess_pdf

api_key = settings.API_KEY


class DocumentCreateView(generics.CreateAPIView):
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"document_id": instance.id}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            instance = serializer.save()

            preprocess_pdf(instance.file_url.path, instance.file_url.path)
            process_ocr_task_for_essay.delay(instance.id, api_key)

            return instance
        
        except ValidationError as e:
            raise ValidationError(f"유효성 검사 오류: {e}")

        except Exception as e:
            print(f"Error occurred during task execution: {e}")
            raise


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentReasonsSerializer
    pagination_class = None

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        document_type = self.kwargs.get('document_type')
        documents = Document.objects.filter(student_id=student_id, document_type__name=document_type).order_by('-upload_date')
        return documents


class StudentRecordsView(APIView):
    def get(self, request):
        student_records = Documentation.objects.filter(document_type__name='학생생활기록부', state="제출").order_by('upload_date').values("id")
        answer = []
        for record in student_records:
            answer.append(record['id'])
        return Response(answer)


class StudentRecordDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SummarizationSerializer

    def get_object(self):
        record_id = self.kwargs.get('record_id')
        try:
            summarization = Summarization.objects.get(document=record_id)
        except Summarization.DoesNotExist:
            raise NotFound(f"{record_id}: 해당 id의 학생생활기록부 요약본을 찾을 수 없습니다.")
        return summarization


class EssaysView(APIView):
    def get(self, request):
        essays = Document.objects.filter(document_type='논술').order_by('upload_date').values("id")
        answer = []
        for essay in essays:
            answer.append(essay['id'])
        return Response(answer)


class EssayDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = EvaluationSerializer

    def get_object(self):
        essay_id = self.kwargs.get('essay_id')
        try:
            evaluation = Evaluation.objects.get(document=essay_id)
        except Evaluation.DoesNotExist:
            raise NotFound(f"{essay_id}: 해당 id의 논술 평가본을 찾을 수 없습니다.")
        return evaluation


class EssayCriteriaView(generics.RetrieveAPIView):
    serializer_class = EssayCriteriaSerializer

    def get_object(self):
        essay_id = self.kwargs.get('essay_id')
        try:
            document = Document.objects.get(id=essay_id)
        except Evaluation.DoesNotExist:
            raise NotFound(f"{essay_id}: 해당 id의 논술 파일일을 찾을 수 없습니다.")
        criteria = document.criteria
        return criteria
    

class DocumentStateAPIView(APIView):
    def patch(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentStatusSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Document state updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentWithReasonsAPIView(APIView):
    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentReasonsSerializer(document)
        return Response(serializer.data)


class DocumentationCreateView(generics.CreateAPIView):
    serializer_class = DocumentationSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()

            if not instance.file_url:
                raise ValidationError("파일이 업로드되지 않았습니다.")

            allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
            if not any(instance.file_url.name.lower().endswith(ext) for ext in allowed_extensions):
                raise ValidationError("지원되지 않는 파일 형식입니다. PDF, PNG, JPG만 가능합니다.")

            
            process_inference.delay(instance.id)
            process_ocr_task.delay(instance.id, api_key)

            return instance
        
        except ValidationError as e:
            raise ValidationError(f"유효성 검사 오류: {e}")

        except Exception as e:
            print(f"Error occurred during task execution: {e}")
            raise
    
