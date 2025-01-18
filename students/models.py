from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=10)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name

class Department(models.Model):
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.department

class Applicant(models.Model):
    application_type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)