from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Student
from documents.models import DocumentTypeChoices, DocumentStateChoices

class StudentListSerializer(ModelSerializer):
    department = SerializerMethodField()
    documents = SerializerMethodField()

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'department', 'phone', 'documents']

    def get_department(self, obj):
        return obj.department.department
    
    def get_documents(self, obj):
        ans = dict()
        documents = obj.documents.all()
        for document_type in DocumentTypeChoices.values:
            document_list = documents.filter(document_type=document_type).order_by('-upload_date')
            if not document_list:
                ans[document_type] = DocumentStateChoices.미제출
            else:
                ans[document_type] = document_list[0].state if document_list[0].state else DocumentStateChoices.미제출
        return ans