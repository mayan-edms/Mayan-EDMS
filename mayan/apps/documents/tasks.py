import logging

from mayan.celery import app

from .models import Document

logger = logging.getLogger(__name__)


@app.task
def task_get_document_image(document_id, *args, **kwargs):
    document = Document.objects.get(pk=document_id)
    return document.get_image(*args, **kwargs)
