from django.db import models

# Create your models here.
class DocumentTypeChoices(models.TextChoices):
    검정고시 = '검정고시', '검정고시'
    생활기록부대체양식 = '생활기록부대체양식', '생활기록부대체양식'
    기초생활수급자 = '기초생활수급자', '기초생활수급자'
    주민등록본 = '주민등록본', '주민등록본'
    국민체력100 = '국민체력100', '국민체력100'
    체력평가 = '체력평가', '체력평가'
    학생생활기록부 = '학생생활기록부', '학생생활기록부'
    논술 = '논술', '논술'

class DocumentStateChoices(models.TextChoices):
    미제출 = '미제출', '미제출'
    검토 = '검토', '검토'
    제출 = '제출', '제출' 

class Document(models.Model):
    document_type = models.CharField(max_length=50)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documents')
    upload_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=DocumentStateChoices.choices, default=DocumentStateChoices.미제출)

    def upload_to(self, filename):
        return f'documents/{self.document_type}/{filename}'

    file_url = models.FileField(upload_to=upload_to)

    def __str__(self):
        return f"{self.student}의 {self.document_type}({self.state})"