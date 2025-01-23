from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import NotFound

from rest_framework import generics
from .models import Document
from aims.models import Summarization, Evaluation

from .serializers import DocumentSerializer, DocumentReasonsSerializer
from aims.serializers import EvaluationSerializer, SummarizationSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status

# Create your views here.
class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"document_id": instance.id}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentReasonsSerializer
    pagination_class = None

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        document_type = self.kwargs.get('document_type')
        documents = Document.objects.filter(student_id=student_id, document_type=document_type).order_by('-upload_date')
        return documents

class StudentRecordsView(APIView):
    def get(self, request):
        student_records = Document.objects.filter(document_type='학생생활기록부', state="제출").order_by('upload_date').values("id")
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