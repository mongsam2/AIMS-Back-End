import os

from celery import shared_task
from django.conf import settings
from .models import Documentation, Document

from aims.models import Extraction, ExtractionEssay
from aims.utils.execute_apis import execute_ocr, get_answer_from_solar


@shared_task
def process_ocr_task(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        #document = RawData.objects.get(id=document_id)
        document = Documentation.objects.get(id=document_id)
        content, confidence = execute_ocr(api_key, document.file_url.path)
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
        content, confidence = execute_ocr(api_key, document.file_url.path)
        
        prompt_path = os.path.join(settings.BASE_DIR, 'aims', 'utils', 'prompt_txt', 'refine_prompt.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()

        refined_content = get_answer_from_solar(api_key, content, prompt)
        ExtractionEssay.objects.create(content=refined_content, document=document)
            
    except Document.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")
