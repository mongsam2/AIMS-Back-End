import os

from celery import shared_task
from django.conf import settings
from .models import Documentation, Document, DocumentType, DocumentStateChoices

from aims.models import Extraction, ExtractionEssay
from aims.utils.execute_apis import execute_ocr, get_answer_from_solar

from documents.utils.inference_with_pytorch import predict_document_type
from documents.utils.inference_onnx import predict_onnx


@shared_task
def process_ocr_task(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        #document = RawData.objects.get(id=document_id)
        document = Documentation.objects.get(id=document_id)
        content = execute_ocr(api_key, document.file_url.path)
        Extraction.objects.create(content=content, document=document)
            

    #except RawData.DoesNotExist:
    except Documentation.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")


@shared_task
def process_ocr_task_for_essay(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        document = Document.objects.get(id=document_id)
        content = execute_ocr(api_key, document.file_url.path)
        
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
def process_inference(document_id):
    """
    비동기 inference 작업 수행

    Args:
        document_id (Documentation): Documentation 테이블의 인스턴스
    """
    try:
        document = Documentation.objects.get(id=document_id)
        class_labels = settings.LABELS
        
        d_type, confidence = predict_document_type(document.file_url.path, class_labels)
        #d_type, confidence = predict_onnx(document.file_url.path, class_labels)

        matched_document_type = DocumentType.objects.filter(name=d_type).first()

        if matched_document_type:
            document.document_type = matched_document_type.name
            document.state = DocumentStateChoices.제출
            document.save()
            print(f"🟢 문서 {document_id}의 유형이 '{matched_document_type}'로 업데이트되었습니다.")
        else:
            document.state = DocumentStateChoices.검토
            document.save()
            print(f"🟡 문서 {document_id}: '{d_type}'를 DocumentType에서 찾을 수 없어 상태를 '검토'로 변경.")

        return f"Inference 성공: 문서 {document_id} → {matched_document_type if matched_document_type else '검토'}"

    except Documentation.DoesNotExist:
        return f"문서 {document_id}를 찾을 수 없습니다."
    
    except Exception as e:
        return f"Inference 실패: {str(e)}"