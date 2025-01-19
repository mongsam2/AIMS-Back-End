from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Document, DocumentTypeChoices
from aims.models import Summarization
from aims.serializers import ReasonsSerializer

class DocumentSerializer(ModelSerializer):
    '''
    새로운 파일을 업로드할 때, 사용하는 Serializer
    '''
    class Meta:
        model = Document
        exclude = ['memo', 'state']

    def validate_document_type(self, value):
        if value not in DocumentTypeChoices:
            raise serializers.ValidationError(f'{value}는 존재하지 않는 서류의 유형입니다.')
        return value

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
        