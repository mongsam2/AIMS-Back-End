import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from documents.models import Documentation, DocumentStateChoices
from aims.models import Extraction, ValidationCriteria
from students.models import Student

from aims.tasks import get_answer_from_solar, execute_embedding
from documents.utils.validate_docs import is_date_valid, is_doc_type_valid, similarity

from django.conf import settings


@receiver(post_save, sender=Extraction)
def assign_student_id_and_issue_date(sender, instance, **kwargs):
    """
    Extraction 테이블에 새로운 값이 저장되면 Signal이 트리거됨
    
    1. OCR에서 추출한 학생 이름을 기반으로 Student ID 할당
    2. 서류 발행일자 저장 및 유효성 확인

    """
    api_key = settings.API_KEY

    content = instance.content
    prompt = '넌 지금 서류의 주인이 누군지 찾고 서류 발행일자를 알아내서 쉼표로 구분한 문자열로 반환해줘야 해. 서류 주인의 이름을 문자열로 첫 번째에, 발행일자를 "YYYY-MM-DD" 형식 문자열로 두 번째에 반환하는데, 서류 주인의 생년월일과 헷갈리지 말고 서류를 발행한 날짜를 반환해줘'
    answer = get_answer_from_solar(api_key, content, prompt)

    answer_list = list(answer.split(", "))

    extracted_names = answer_list[0].rstrip()
    date = answer_list[1].rstrip()

    print(answer)
    print(extracted_names, date)

    documentation = Documentation.objects.filter(extraction=instance).first()

    if not documentation:
        print("연결된 Documentation을 찾을 수 없습니다.")
        return

    # 1. student_id 찾기
    if extracted_names:
        student_name = extracted_names
        student = Student.objects.filter(name=student_name).first()
        
        if student:
            documentation.student_id = student
            print(f"학생 '{student_name}'의 student_id({student.student_id})가 Documentation에 저장되었습니다.")
        else:
            print(f"학생 '{student_name}'을 Student 테이블에서 찾을 수 없습니다.")

    # 2. issue_date 확인
    documentation.issue_date = date

    if not is_date_valid(date):
        documentation.state = DocumentStateChoices.검토
        print(f"발행 일자: {date} -> 문서 검토가 필요합니다.")

    documentation.save()


@receiver(post_save, sender=Documentation)
def get_doc_attributes(sender, instance, **kwargs):
    """
    Documentation의 document_type 변경을 감지하여 ValidationCriteria 조건을 확인하고,
    조건이 만족되면 state를 '제출'로 변경하는 Signal
    """
    if instance.tracker.has_changed('document_type'):
        new_value = instance.document_type

        validation_criteria = ValidationCriteria.objects.filter(document_type=new_value)

        if not validation_criteria.exists():
            print(f"{new_value}에 대한 ValidationCriteria가 없음 → 상태 변경 안 함")
            return

        extraction = Extraction.objects.filter(document=instance).first()
        
        if not extraction:
            print(f"{instance.id}에 해당하는 Extraction이 없습니다.")
            return

        # Extraction 내용에서 v_condition 값이 포함되어 있는지 확인
        valid = all(criterion.v_condition in extraction.content for criterion in validation_criteria)
        new_state = DocumentStateChoices.제출 if valid else DocumentStateChoices.검토

        Documentation.objects.filter(id=instance.id).update(state=new_state)
        print(f"문서 {instance.id}의 상태가 '{new_state}'로 변경됨")
    

@receiver(post_save, sender=Extraction)
def save_embedding_vector(sender, instance, **kwargs):
    
    if not instance.content:
        print(f"Extraction {instance.id}의 content가 비어있음. 벡터 변환을 건너뜁니다.")
        return
    
    try:
        api_key = settings.API_KEY
        content = instance.content
        
        text_vectors = execute_embedding([content], api_key)
        vector = json.dumps(text_vectors)

        Extraction.objects.filter(id=instance.id).update(vector=vector)
        print(f"Extraction {instance.id}의 OCR 벡터 저장 완료")

    except Exception as e:
        print(f"벡터 변환 중 오류 발생: {e}")


@receiver(post_save, sender=Extraction)
def save_extraction_type(sender, instance, **kwargs):
    if not instance.vector:
        print(f"Extraction {instance.id}의 vector가 비어있음")
        return

    try:
        # json 파일로 기존 문서 벡터 불러오기
        queries = {}

        text_vectors = json.loads(instance.vector)

        document_type = similarity(queries, text_vectors)
        Extraction.objects.filter(id=instance.id).update(document_type=document_type)
    except Exception as e:
        print(f"유사도 계산 오류 발생: {e}")

