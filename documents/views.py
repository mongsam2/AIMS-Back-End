# Views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

# Serializers
from .serializers import DocumentUploadSerializer

# Utils
from utils.upstage import execute_ocr
from utils.document import predict_document_type, extract_student_number
from django.conf import settings
import os

# Exceptions
from rest_framework.exceptions import ParseError, NotFound

from common.models import DocumentType
from students.models import Student

# Create your views here.
class DocumentUploadView(GenericAPIView, CreateModelMixin):
    serializer_class = DocumentUploadSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
        
        api_key = settings.UPSTAGE_API_KEY
        excuted_text, confidence = execute_ocr(api_key, document.file.file)
        document_type, confidence = predict_document_type(document.file.path)
        student_id = extract_student_number(excuted_text)[1]
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise NotFound(f"학생번호 {student_id}에 해당하는 학생이 존재하지 않습니다.")
        try:
            document_type = DocumentType.objects.get(name=document_type)
        except DocumentType.DoesNotExist:
            raise NotFound(f"판별한 {document_type}이 존재하지 않습니다.")
        document.extraction = excuted_text
        document.document_type = document_type
        document.student = student
        document.save()
        return Response({"detail": "성공이야"})