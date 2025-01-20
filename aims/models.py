from django.db import models
from documents.models import Document

# Create your models here.
class Extraction(models.Model):
    content = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

class InappropriateReason(models.Model):
    content = models.CharField(max_length=100)
    page = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reasons') 

    def __str__(self):
        return f"{self.document} 부적합 이유"

class Evaluation(models.Model):
    content = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.document} 평가"

class Summarization(models.Model):
    content = models.TextField()
    question = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    memo = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return f"{self.document} 요약"