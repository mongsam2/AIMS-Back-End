from django.db import models

# Create your models here.
class Document(models.Model):
    document_type = models.CharField(max_length=50)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def upload_to(self, filename):
        return f'documents/{self.document_type}/{filename}'

    file_url = models.FileField(upload_to=upload_to)

    def __str__(self):
        return self.document_type


class DocumentTypeChoices(models.TextChoices):
    학생생활기록부 = '학생생활기록부', '학생생활기록부'
    검정고시 = '검정고시', '검정고시'
    국외고등학교 = '국외고등학교', '국외고등학교'
    기초생활수급자 = '기초생활수급자', '기초생활수급자'
    차상위계층 = '차상위계층', '차상위계층'
    농어촌학생 = '농어촌학생', '농어촌학생'