import os
from django.db import models

from documents.utils.essay_preprocess import preprocess_pdf

API_KEY = os.environ.get('UPSTAGE_API_KEY')


class DocumentTypeChoices(models.TextChoices):
    학생생활기록부 = '학생생활기록부', '학생생활기록부'
    검정고시합격증명서 = '검정고시합격증명서', '검정고시합격증명서'
    생활기록부대체양식 = '생활기록부대체양식', '생활기록부대체양식'
    수급자증명서 = '기초생활수급자증명서', '기초생활수급자증명서'
    주민등록본 = '주민등록본', '주민등록본'
    국민체력100인증서 = '국민체력100인증서', '국민체력100인증서'
    체력평가 = '체력평가', '체력평가'
    논술 = '논술', '논술'
    알수없음 = '알수없음', '알수없음'


class DocumentStateChoices(models.TextChoices):
    미제출 = '미제출', '미제출'
    검토 = '검토', '검토'
    제출 = '제출', '제출' 


class Document(models.Model):
    #document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DocumentTypeChoices.choices, default=DocumentTypeChoices.알수없음)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='documents')
    upload_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=DocumentStateChoices.choices, default=DocumentStateChoices.미제출)
    criteria = models.ForeignKey('aims.EssayCriteria', on_delete=models.CASCADE, null=True, blank=True)


    def upload_to(self, filename):
        return f'documents/{self.document_type}/{filename}'


    file_url = models.FileField(upload_to=upload_to)


    def __str__(self):
        return f"{self.student}의 {self.document_type}({self.state})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.process_ocr_and_validation()
        
        # 논술 데이터 전처리
        if self.document_type == "논술":
            preprocess_pdf(self.file_url.path, self.file_url.path)


    def process_ocr_and_validation(self):
        
        # OCR 후 Extraction에 저장
        from aims.utils.execute_apis import execute_ocr
        content = execute_ocr(API_KEY, self.file_url.path)

        from aims.models import Extraction
        extraction = Extraction.objects.create(document=self, content=content)

        # Student 찾아서 저장
        student_name = self.extract_student_name(content)
        if student_name:
            from students.models import Student
            student = Student.objects.filter(name=student_name).first()
            if student:
                self.student = student
                self.save()

        # ValidationCriteria 검증
        self.validate_extraction(extraction)


    # OCR 결과에서 학생 이름 추출 로직
    def extract_student_name(self, content):
        import re
        match = re.search(r"학생 이름: (\S+)", content) 
        return match.group(1) if match else None


    def validate_extraction(self, extraction):
        from aims.models import ValidationCriteria
        failed_conditions = []

        # 해당 document_type의 검증 조건 가져오기
        criteria = ValidationCriteria.objects.filter(document_type=self.document_type.name)
        for criterion in criteria:
            if criterion.v_condition not in extraction.content:
                failed_conditions.append(criterion.v_condition)

        # 적합 여부 처리
        if failed_conditions:
            self.state = DocumentStateChoices.검토
            print(f"부적합 조건: {failed_conditions}")
        else:
            self.state = DocumentStateChoices.제출
            print("적합 -> 제출 완료")
        
        self.save()


class DocumentType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name