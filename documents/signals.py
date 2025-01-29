from django.db.models.signals import post_save
from django.dispatch import receiver
from documents.models import Documentation, DocumentStateChoices, DocumentType
from aims.models import Extraction, ValidationCriteria
from students.models import Student

from aims.utils.get_student_name import extract_student_name

@receiver(post_save, sender=Extraction)
def assign_student_id_and_document_type(sender, instance, **kwargs):
    """
    Extraction 테이블에 값이 저장되면 Signal이 트리거됨.
    1️⃣ OCR에서 추출한 학생 이름을 기반으로 Student ID 할당
    2️⃣ ValidationCriteria에서 문서 유형을 찾아 DocumentType 테이블에서 검색 후 Documentation에 설정
    3️⃣ 문서 유형을 찾을 수 없으면 상태를 '검토'로 변경
    """

    content = instance.content
    extracted_names = extract_student_name(content)

    documentation = Documentation.objects.filter(extraction=instance).first()

    if not documentation:
        print("🔴 연결된 Documentation을 찾을 수 없습니다.")
        return

    # 1️⃣ 학생 ID 찾기
    if extracted_names:
        student_name = extracted_names[0]
        student = Student.objects.filter(name=student_name).first()
        if student:
            documentation.student_id = student
            print(f"🟢 학생 '{student_name}'의 student_id({student.student_id})가 Documentation에 저장되었습니다.")
        else:
            print(f"🔴 학생 '{student_name}'을 Student 테이블에서 찾을 수 없습니다.")

    # 2️⃣ 문서 유형 할당 (ValidationCriteria 기준 + DocumentType 테이블에서 검색)
    matched_document_type = None
    validation_criteria = ValidationCriteria.objects.all()

    for criteria in validation_criteria:
        if criteria.v_condition in content:
            matched_document_type = DocumentType.objects.filter(name=criteria.document_type).first()
            break  # 첫 번째 일치하는 문서 유형만 사용

    if matched_document_type:
        documentation.document_type = matched_document_type.name  # 🔴 여기서 .name을 사용 (문자열 저장)
        documentation.state = DocumentStateChoices.제출  # 문서 유형을 찾았으므로 제출 상태로 변경
        print(f"🟢 문서 유형 '{matched_document_type.name}'이 DocumentType 테이블에서 검색되어 할당되었습니다.")
    else:
        documentation.state = DocumentStateChoices.검토  # 문서 유형을 찾지 못했으므로 검토 상태로 변경
        print("🟠 문서 유형을 찾을 수 없습니다. 상태를 '검토'로 변경합니다.")

    # 변경된 내용 저장
    documentation.save()
