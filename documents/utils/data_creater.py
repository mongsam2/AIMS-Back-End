from celery import chain

from django.conf import settings

from aims.tasks import execute_ocr, get_answer_from_solar

from documents.models import Documentation, Document
from documents.tasks import predict_pytorch, update_document_type, save_ocr_result


def process_inference(document_id):
    """
    inference 작업 수행 후 문서 타입 저장

    Args:
        document_id (Documentation): Documentation 테이블의 인스턴스
    """
    try:
        document = Documentation.objects.get(id=document_id)
        class_labels = settings.LABELS

        workflow = chain(
            predict_pytorch.s(document.file_url.path, class_labels),
            update_document_type.s(document_id)
        )
        
        workflow.apply_async()
        
        return f"Inference 태스크 시작: 문서 {document_id}"

    except Documentation.DoesNotExist:
        return f"문서 {document_id}를 찾을 수 없습니다."

    except Exception as e:
        return f"Inference 실패: {str(e)}"
    

def process_ocr_task(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        print(f"Documnet ID {document_id} OCR 추출중...")
        document = Documentation.objects.get(id=document_id)

        workflow = chain(
            execute_ocr.s(api_key, document.file_url.path),
            save_ocr_result.s(document_id),
        )
        
        workflow.apply_async()
            
    except Documentation.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")