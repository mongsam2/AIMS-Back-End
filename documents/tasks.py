import os
import json
import torch
import numpy as np

from celery import shared_task

from django.conf import settings

from aims.tasks import execute_ocr, get_answer_from_solar

from students.models import Student
from .models import Documentation, Document, DocumentType, DocumentStateChoices
from aims.models import Extraction, ExtractionEssay, DocumentPassFail, FailedConditionChoices

from documents.utils.load_model import load_pytorch_model, load_onnx_model
from documents.utils.data_loader import preprocess_image
from documents.utils.validate_docs import is_date_valid, similarity, is_doc_type_valid, cosine_similarity_manual
from documents.utils.attribute_getter import get_name_and_date


@shared_task
def save_ocr_result(result, document_id):
    """
    OCR 결과를 저장하는 후처리 작업
    """
    try:
        content, confidence = result
        document = Documentation.objects.get(id=document_id)
        Extraction.objects.create(document=document, content=content)

    except Documentation.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error saving OCR result for Document ID {document_id}: {str(e)}")
    

@shared_task
def save_name_and_date(result, instance_id):
    try:
        documentation = Documentation.objects.filter(extraction=instance_id).first()
        
        if not documentation:
            print("연결된 Documentation을 찾을 수 없습니다.")
            return
        try:
            name, date, title = get_name_and_date(result)
        except ValueError:
            print(f"잘못된 형식: {result}")
            return

        # 1. student_id 찾기
        if name:
            student_name = name
            student = Student.objects.filter(name=student_name).first()
            
            if student:
                documentation.student_id = student
                print(f"학생 '{student_name}'의 student_id({student.student_id})가 Documentation에 저장되었습니다.")
            else:
                failed_condition = FailedConditionChoices.UNAUTHORIZED_APPLICANT
                DocumentPassFail.objects.create(document_id=documentation, is_valid=False, content=failed_condition)
                documentation.state = DocumentStateChoices.검토
                print(f"학생 '{student_name}'을 Student 테이블에서 찾을 수 없습니다.")

        # 2. issue_date 확인
        documentation.issue_date = date

        if not is_date_valid(date):
            failed_condition = FailedConditionChoices.INVALID_DATE
            DocumentPassFail.objects.create(document_id=documentation, is_valid=False, content=failed_condition)
            documentation.state = DocumentStateChoices.검토
            print(f"발행 일자: {date} -> 문서 검토가 필요합니다.")

        Extraction.objects.filter(id=instance_id).update(title=title)

        documentation.save()
        return f"문서 {documentation.id} 업데이트 완료."
    
    except Exception as e:
        return f"저장 실패: {str(e)}"
    

@shared_task
def save_vectors(result, instance_id):
    try:
        vector = json.dumps(result)
        updated_rows = Extraction.objects.filter(id=instance_id).update(vector=vector)
        if updated_rows > 0:
            print(f"Extraction {instance_id}의 OCR 벡터 저장 완료")
        else:
            print(f"Extraction {instance_id}을 찾을 수 없어 벡터 저장 실패")
    except Exception as e:
        print(f"Extraction {instance_id} 벡터 저장 중 오류 발생: {e}")


@shared_task
def save_extraction_type(result, instance_id):
    try:
        instance = Extraction.objects.get(id=instance_id)
        queries = np.array(json.loads(instance.vector))
        
        # Extraction과 연결된 Documentation 찾기
        documentation = Documentation.objects.filter(extraction=instance_id).first()
        if not documentation:
            print(f"Extraction {instance_id}에 연결된 Documentation을 찾을 수 없습니다.")
            return
        
        doc_type = documentation.document_type
        if not doc_type:
            print(f"문서 {instance_id}의 document_type이 설정되지 않음.")
            return

        # OCR 벡터값과 기존 문서 벡터 비교
        json_path = "/data/ephemeral/home/aims_be/documents/vectors/validations2.json"
        with open(json_path, "r", encoding="utf-8") as file:
            validation_data = json.load(file)

        matched_document = next((doc for doc in validation_data if doc["document_type"] == doc_type), None)

        if not matched_document:
            print(f"{doc_type}에 해당하는 validation_data를 찾을 수 없습니다.")
            return
        
        text_vectors = np.array(matched_document.get("vector", []))
        if text_vectors.size == 0:
            print(f"⚠️ {doc_type}의 벡터 정보가 없음.")
            return

        similarities = cosine_similarity_manual(queries, text_vectors)

        best_similarity = np.max(similarities)

        print(f"{doc_type} 최고 유사도: {best_similarity:.4f}")

        similarity_threshold = settings.SIMILARITY_THRESHOLD
        
        if best_similarity >= similarity_threshold:
            documentation.state = DocumentStateChoices.제출
        else:
            documentation.state = DocumentStateChoices.검토
            DocumentPassFail.objects.create(
                document_id=documentation,
                is_valid=False,
                content=FailedConditionChoices.UNMATCHED_DOC_TYPE
            )
            print(f"문서 {instance_id} 검토 필요 (유사도: {best_similarity:.4f})")

        documentation.save(update_fields=["state"])

    except Extraction.DoesNotExist:
        print(f"Extraction {instance_id}을 찾을 수 없습니다.")
    except Exception as e:
        print(f"유사도 계산 오류 발생: {e}")


@shared_task
def double_check_doc_type(instance_id):
    """
    Extraction 테이블의 document_type과 Documentation 테이블의 document_type을 비교하여
    상태(state)를 '제출' 또는 '검토'로 변경하고 사유를 DocumentPassFail에 저장하는 비동기 태스크
    """
    try:
        # Extraction과 연결된 Documentation 찾기
        documentation = Documentation.objects.filter(extraction=instance_id).first()
        extraction = Extraction.objects.get(id=instance_id)

        if not documentation:
            print(f"Extraction {instance_id}에 연결된 Documentation을 찾을 수 없습니다.")
            return

        if not extraction.document_type:
            print(f"Extraction {instance_id}의 document_type이 비어 있음")
            return

        # 문서 유형 검증
        valid = is_doc_type_valid(documentation.document_type, extraction.document_type)
        
        if valid:
            new_state = DocumentStateChoices.제출
            print(f"문서 {documentation.id}의 상태가 '제출'로 변경됨.")
        else:
            new_state = DocumentStateChoices.검토
            failed_condition = FailedConditionChoices.UNMATCHED_DOC_TYPE
            DocumentPassFail.objects.create(
                document_id=documentation,
                is_valid=False,
                content=failed_condition
            )
            print(f"문서 {documentation.id}의 상태가 '검토'로 변경됨. (Extraction과 문서 유형 불일치)")

        # 상태 업데이트
        Documentation.objects.filter(id=documentation.id).update(state=new_state)
        print(f"문서 {documentation.id}의 상태가 '{new_state}'로 업데이트 완료.")

    except Exception as e:
        print(f"문서 유형 검증 중 오류 발생: {e}")


@shared_task
def process_ocr_task_for_essay(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        document = Document.objects.get(id=document_id)
        content, confidence = execute_ocr.delay(api_key, document.file_url.path)
        
        threshold = 0.8

        # OCR 인식률 저하 시 경고 메시지 저장
        if confidence <= threshold:
            warning = f'경고: OCR 신뢰도가 낮습니다 ({confidence:.2f}). 텍스트가 부정확할 수 있습니다.\n'
            ExtractionEssay.objects.create(content=warning, document=document)
        else:
            prompt_path = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'refine_prompt.txt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt = f.read()

            refined_content = get_answer_from_solar(api_key, content, prompt)
            ExtractionEssay.objects.create(content=refined_content, document=document)
            
    except Document.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")
    

@shared_task
def update_document_type(result, document_id):
    """
    문서 유형을 업데이트하는 Celery 태스크

    Args:
        result (tuple): (예측된 문서 유형, 신뢰도 점수)
        document_id (int): 업데이트할 문서의 ID
    """
    try:
        document = Documentation.objects.get(id=document_id)
        d_type, confidence = result  # predict_pytorch의 결과 (문서 유형, 신뢰도)

        matched_document_type = DocumentType.objects.filter(name=d_type).first()

        if matched_document_type:
            document.document_type = matched_document_type.name
            document.confidence = confidence
            document.state = DocumentStateChoices.제출
            document.save()
            print(f"문서 {document_id}의 유형이 '{matched_document_type.name}'로 업데이트됨.")
        else:
            document.state = DocumentStateChoices.검토
            document.save()
            print(f"문서 {document_id}: '{d_type}'를 DocumentType에서 찾을 수 없어 상태를 '검토'로 변경.")

        return f"문서 {document_id} 업데이트 완료: {matched_document_type.name if matched_document_type else '검토'}"

    except Documentation.DoesNotExist:
        return f"문서 {document_id}를 찾을 수 없습니다."

    except Exception as e:
        return f"문서 업데이트 실패: {str(e)}"
    

@shared_task
def predict_pytorch(file_path, class_labels):
    
    model = load_pytorch_model()
    model.eval()

    image = preprocess_image(file_path)
    
    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()

    predicted_label = class_labels[predicted_class]
    confidence = probabilities[0][predicted_class].item()

    print(predicted_label, confidence)
    
    return predicted_label, confidence


@shared_task
def predict_onnx(image_path, class_labels):
    
    session = load_onnx_model()
    image = preprocess_image(image_path)
    
    inputs = {session.get_inputs()[0].name: image}
    output = session.run(None, inputs)[0]

    predicted_class = np.argmax(output, axis=1).item()
    confidence = np.max(output).item()

    return class_labels[predicted_class], confidence