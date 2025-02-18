from rest_framework.serializers import ModelSerializer
from .models import Document, Documentation
from aims.serializers import DocumentPassFailSerializer


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


class DocumentationSerializer(ModelSerializer):
    class Meta:
        model = Documentation
        fields = ('id', 'student_id', 'document_type', 'file_url', 'state', 'issue_date')

        