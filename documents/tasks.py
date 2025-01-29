import os
from celery import shared_task
from .models import RawData, Documentation
from aims.models import Extraction
from aims.utils.execute_apis import execute_ocr


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


