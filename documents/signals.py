import json
import numpy as np
from celery import chain

from django.db.models.signals import post_save
from django.dispatch import receiver
from documents.models import Documentation, DocumentStateChoices
from aims.models import Extraction, ValidationCriteria, DocumentPassFail, FailedConditionChoices

from aims.tasks import get_answer_from_solar, execute_embedding
from documents.tasks import save_name_and_date, save_vectors, save_extraction_type, double_check_doc_type

from django.conf import settings


# @receiver(post_save, sender=Extraction)
# def assign_student_id_and_issue_date(sender, instance, **kwargs):
#     """
#     Extraction 테이블에 새로운 값이 저장되면 Signal이 트리거됨
    
#     1. OCR에서 추출한 학생 이름을 기반으로 Student ID 할당
#     2. 서류 발행일자 저장 및 유효성 확인

#     """
#     try:
#         api_key = settings.API_KEY

#         content = instance.content
#         prompt = '넌 지금 서류의 주인이 누군지 찾고 서류 발행일자를 알아내서 쉼표로 구분한 문자열로 반환해줘야 해. 서류 주인의 이름을 문자열로 첫 번째에, 발행일자를 "YYYY-MM-DD" 형식 문자열로 두 번째에 반환하는데, 서류 주인의 생년월일과 헷갈리지 말고 서류를 발행한 날짜를 반환해줘'

#         workflow = chain(
#             get_answer_from_solar.s(api_key, content, prompt),
#             save_name_and_date.s(instance.id)
#         )

#         workflow.apply_async()

#     except Exception as e:
#         print(f"이름/날짜 저장 실패: {str(e)}")

    

@receiver(post_save, sender=Extraction)
def process_embedding_vector(sender, instance, **kwargs):
    if not instance.content:
        print(f"Extraction {instance.id}의 content가 비어있음. 벡터 변환을 건너뜁니다.")
        return
    
    try:
        api_key = settings.API_KEY
        content = instance.content

        prompt = '넌 지금 서류의 주인이 누군지 찾고 서류 발행일자, 서류의 제목을 알아내서 쉼표로 구분한 문자열로 반환해줘야 해. 서류 주인의 이름을 문자열로 첫 번째에, 발행일자를 "YYYY-MM-DD" 형식 문자열로 두 번째에 반환하는데, 서류 주인의 생년월일과 헷갈리지 말고 서류를 발행한 날짜를 반환해야해. 세 번째에는 문서 제목에 해당하는 글자를 반환해줘.'
        
        workflow = chain(
            get_answer_from_solar.s(api_key, content, prompt),
            save_name_and_date.s(instance.id),
            execute_embedding.s([content], api_key),
            save_vectors.s(instance.id),
            save_extraction_type.s(instance.id),
            double_check_doc_type.s(instance.id)
        )

        workflow.apply_async()

    except Exception as e:
        print(f"벡터 변환 중 오류 발생: {e}")
