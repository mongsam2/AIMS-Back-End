from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Document, RawData, DocumentTypeChoices
from aims.models import Summarization
from students.models import Student
from aims.serializers import DocumentPassFailSerializer
import os


class DocumentSerializer(ModelSerializer):
    '''
    새로운 파일을 업로드할 때, 사용하는 Serializer
    '''
    class Meta:
        model = Document
        fields = ('file_url', 'document_type', 'student', 'criteria')


class DocumentStatusSerializer(ModelSerializer):
    class Meta:
        model = Document
        fileds = ['state']


class DocumentReasonsSerializer(ModelSerializer):
    reasons = DocumentPassFailSerializer(many=True)

    class Meta:
        model = Document
        fields = ['state', 'file_url', 'reasons']


class StudentRecordsSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ['id']


class RawDataSerializer(ModelSerializer):
    '''
    새로운 파일을 업로드할 때, 사용하는 Serializer
    '''
    class Meta:
        model = RawData
        fields = ('file_url')
        