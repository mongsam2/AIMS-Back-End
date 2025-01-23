from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Document, DocumentTypeChoices
from aims.models import Summarization
from students.models import Student
from aims.serializers import ReasonsSerializer
import os

class DocumentSerializer(ModelSerializer):
    '''
    새로운 파일을 업로드할 때, 사용하는 Serializer
    '''
    class Meta:
        model = Document
        fields = ('file_url',)

    def validate_file_url(self, value):
        lst = value.name.split('_')
        if len(lst) != 2:
            raise serializers.ValidationError('파일 이름이 올바르지 않습니다.')
        
        student_id, document_type = lst
        if Student.objects.filter(student_id=student_id).exists() == False:
            raise serializers.ValidationError('해당 학생이 존재하지 않습니다.')
        
        document_type = document_type.split('.')[0]
        if document_type not in DocumentTypeChoices.values:
            raise serializers.ValidationError('해당 서류의 유형이 존재하지 않습니다.')
        
        return value

    def create(self, validated_data):
        file_url = validated_data['file_url'].name
        file_name = os.path.basename(file_url)
        student_id, document_type = file_name.split('_')
        document_type = document_type.split('.')[0]
        student = Student.objects.get(student_id=student_id)
        document = Document.objects.create(student=student, document_type=document_type, file_url=validated_data['file_url'])
        return document

class DocumentStatusSerializer(ModelSerializer):
    class Meta:
        model = Document
        fileds = ['state']

class DocumentReasonsSerializer(ModelSerializer):
    reasons = ReasonsSerializer(many=True)

    class Meta:
        model = Document
        fields = ['file_url', 'reasons']

class StudentRecordsSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['id']
        