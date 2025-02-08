from django.db import models
from documents.models import Document, Documentation


class FailedConditionChoices(models.TextChoices):
    NONE = 'none', '해당사항 없음'
    INVALID_DATE = 'date', '유효하지 않은 서류 발행일'
    UNMATCHED_DOC_TYPE = 'type', '서류 타입 검증 불일치'
    UNKNOWN_APPLICANT = 'unknown', '일치하는 이름이 명단에 없음'
    MISSING_REQUIRED_FIELD = 'missing_field', '필수 정보 누락'
    UNAUTHORIZED_APPLICANT = 'unauthorized', '대상자가 아닌 신청자'
    INVALID_INFOMATION = 'invalid_infomation', '정보 누락 또는 불일치'


class Extraction(models.Model):
    document = models.ForeignKey(Documentation, on_delete=models.CASCADE, related_name='extraction')
    content = models.TextField()
    vector = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Extraction for {self.document.id}"
    

class ExtractionEssay(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='extraction_essay')
    content = models.TextField()

    def __str__(self):
        return f"Extraction for {self.document.id}"


class DocumentPassFail(models.Model):
    document_id = models.ForeignKey(Documentation, on_delete=models.CASCADE, related_name='reasons') 
    is_valid = models.BooleanField(default=False)
    content = models.CharField(max_length=50, choices=FailedConditionChoices.choices, default=FailedConditionChoices.NONE)

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
    document = models.ForeignKey(Documentation, on_delete=models.CASCADE)
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