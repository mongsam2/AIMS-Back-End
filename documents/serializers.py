from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Document, DocumentTypeChoices

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate_document_type(self, value):
        if value not in DocumentTypeChoices:
            raise serializers.ValidationError(f'{value}는 존재하지 않는 서류의 유형입니다.')
        return value
    
