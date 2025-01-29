from django.db import models
from documents.models import Document, Documentation


class Extraction(models.Model):
    document = models.OneToOneField(Documentation, on_delete=models.CASCADE, related_name='extraction')
    content = models.TextField()

    def __str__(self):
        return f"Extraction for {self.document.id}"


class DocumentPassFail(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='reasons') 
    is_valid = models.BooleanField(default=False)

    page = models.IntegerField()
    failed_conditions = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.document_id} 부적합 이유"


class Evaluation(models.Model):
    content = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)    
    memo = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return f"{self.document} 평가"


class EvaluationRange(models.Model):
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    penalty = models.IntegerField()

    def __str__(self):
        return f"{self.min_value} ~ {self.max_value}: penalty:{self.penalty}점"


class Summarization(models.Model):
    content = models.TextField(null=True, blank=True, default='')
    question = models.TextField(null=True, blank=True, default='')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    memo = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return f"{self.document} 요약"
    

# Criteria
# ─────────────────────────────────────────────────────────────────────────────────────────────


class EssayCriteria(models.Model):
    year = models.IntegerField(default=2025)
    quater = models.IntegerField(default=1, null=True, blank=True)
    content = models.TextField()
    ranges = models.ManyToManyField('EvaluationRange')
    
    def __str__(self):
        return f"{self.year}년도 에세이 평가기준 {self.id}"


class ValidationCriteria(models.Model):
    document_type = models.CharField(max_length=100)
    v_condition = models.TextField()

    def __str__(self):
        return f'{self.document_type} 적합 기준 : {self.v_condition}'