from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Student
from documents.models import DocumentTypeChoices, DocumentStateChoices, DocumentType

class StudentListSerializer(ModelSerializer):
    department = SerializerMethodField()
    documents = SerializerMethodField()

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'department', 'phone', 'documents']

    def get_department(self, obj):
        return obj.department.department
    
    def get_documents(self, obj):
        ans = list()
        documents = obj.documents.all()
        for document_type in DocumentType.objects.values_list('name', flat=True):
            if document_type not in obj.required_documents.values_list('name', flat=True):
                ans.append({"document_type": document_type, "status":None})
                continue
            document_list = documents.filter(document_type=document_type).order_by('-upload_date')
            if not document_list:
                ans.append({"document_type": document_type, "status":"미제출"})
            else:
                ans.append({"document_type":document_type, 
                            "status":document_list[0].state if document_list[0].state else DocumentStateChoices.미제출})
        return ans