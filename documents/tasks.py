import os
from celery import shared_task
from .models import RawData
from aims.models import Extraction
from aims.utils.execute_apis import execute_ocr
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_ocr_task(document_id, api_key):
    """
    비동기 OCR 태스크
    """
    try:
        logger.debug(f"Task started with document_id: {document_id} and api_key: {api_key}")
        document = RawData.objects.get(id=document_id)
        logger.debug(f"Document fetched: {document}")
        
        content = execute_ocr.delay(api_key, document.file_url.path)
        logger.debug(content)

        Extraction.objects.create(content=content, document=document)
        logger.debug("Task completed")

    except RawData.DoesNotExist:
        raise ValueError(f"Document with ID {document_id} does not exist")
    except Exception as e:
        raise ValueError(f"Error processing OCR for Document ID {document_id}: {str(e)}")
