from django.db import models
from documents.models import DocumentType

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=10)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    required_documents = models.ManyToManyField('documents.DocumentType', related_name='students')
    applicant_type = models.ForeignKey('ApplicantType', on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"{self.name}({self.student_id})"

class Department(models.Model):
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.department

class ApplicantType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


# 현재는 사용하지 않음  ------------------------------------------------------------------------------
class Applicant(models.Model):
    application_type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

class ApplicationTypeChoices(models.TextChoices):
    서류형 = '학생부종합전형(서류형)', '학생부종합전형(서류형)'
    면접형 = '학생부종합전형(면접형)', '학생부종합전형(면접형)'
    국방시스템특별전형 = '학생부종합전형(국방시스템특별전형)', '학생부종합전형(국방시스템특별전형)'