import os
from celery import shared_task
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
        content = execute_ocr(api_key, document.file_url.path)[0]
        
        prompt = "Always provide your response in Korean. When performing corrections, only fix spelling, grammar, or word errors that are clearly incorrect in the given context. Do not overcorrect, change the tone, or rewrite sentences unless absolutely necessary. Preserve the original meaning and style as much as possible."

        refined_content = get_answer_from_solar(api_key, content, prompt)
        ExtractionEssay.objects.create(content=refined_content, document=document)
            
    except Document.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")
