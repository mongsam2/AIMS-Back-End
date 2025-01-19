from django.shortcuts import render
from rest_framework import generics
from .models import Student
from documents.models import Document, DocumentTypeChoices, DocumentStateChoices
from .serializers import StudentListSerializer

# Create your views here.
class AplicantsListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer