import os
from django.db import models
from django.conf import settings


api_key = settings.API_KEY


class DocumentTypeChoices(models.TextChoices):
    알수없음 = '알수없음', '알수없음'

    검정고시합격증명서 = '검정고시합격증명서', '검정고시합격증명서'
    국민체력100인증서 = '국민체력100인증서', '국민체력100인증서'
    수급자증명서 = '기초생활수급자증명서', '기초생활수급자증명서'
    주민등록초본 = '주민등록초본', '주민등록초본'
    체력평가 = '체력평가', '체력평가'
    생활기록부대체양식 = '생활기록부대체양식', '생활기록부대체양식'
    
    학생생활기록부 = '학생생활기록부', '학생생활기록부'
    논술 = '논술', '논술'


class DocumentStateChoices(models.TextChoices):
    미제출 = '미제출', '미제출'
    검토 = '검토', '검토'
    제출 = '제출', '제출' 


class Document(models.Model):
    #document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DocumentTypeChoices.choices, default=DocumentTypeChoices.논술)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documents')
    upload_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=DocumentStateChoices.choices, default=DocumentStateChoices.미제출)
    criteria = models.ForeignKey('aims.EssayCriteria', on_delete=models.CASCADE, null=True, blank=True)

    def upload_to(self, filename):
        return f'documents/{self.document_type}/{filename}'

    file_url = models.FileField(upload_to=upload_to)

    def __str__(self):
        return f"{self.student}의 {self.document_type}({self.state})"
    
    
class DocumentType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name
    

class RawData(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)

    def upload_to(instance, filename):
        return f'documents/{filename}'
    
    file_url = models.FileField(upload_to=upload_to)


class Documentation(models.Model):
    student_id = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documentation', default=20250000)
    document_type = models.CharField(max_length=50, choices=DocumentTypeChoices.choices, default=DocumentTypeChoices.알수없음)
    state = models.CharField(max_length=10, choices=DocumentStateChoices.choices, default=DocumentStateChoices.미제출)
    upload_date = models.DateTimeField(auto_now_add=True)

    def upload_to(instance, filename):
        return f'documents/{filename}'
    
    file_url = models.FileField(upload_to=upload_to)

    def __str__(self):
        return f"Documentation for Extraction {self.upload_date}"
    