# View
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

# Serializer
from .serializers import StudentRecordsSerializer

# Models
from .models import StudentRecord
from students.models import Student
from common.models import DocumentType

# Exceptions
from rest_framework.exceptions import NotFound, NotAcceptable

# Create your views here.
class StudentRecordsView(GenericAPIView, CreateModelMixin):
    serializer_class = StudentRecordsSerializer

    def post(self, request):
        '''
        학생생활기록부를 업로드하는 API
            - 파일 이름에 들어있는 수험번호가 현재 존재하지 않으면 404 에러를 반환
        '''
        file = request.data.get('file')
        id, _ = file.name.split('_')

        # 수험번호 검증
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            raise NotFound(f"{id} 학생을 DB에서 찾을 수 없습니다.")
        
        # 기존에 제출 완료된 생기부가 존재 여부 검증
        if StudentRecord.objects.filter(student=student, state="제출").exists():
            raise NotAcceptable(f"{id} 학생의 생기부가 이미 제출되었습니다.")
        
        # DocumentType 검증
        try:
            document_type = DocumentType.objects.get(name='학생생활기록부')
        except DocumentType.DoesNotExist:
            raise NotFound("DocumentType에서'학생생활기록부'을 찾을 수 없습니다.")
        
        return self.create(request, student, document_type)
    
    def create(self, request, student, document_type):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, student, document_type)
        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, student, document_type):
        serializer.save(student=student, document_type=document_type, state="제출")