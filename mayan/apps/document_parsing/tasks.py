import logging

from django.apps import apps

from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_parse_document_file(document_file_pk):
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )
    DocumentPageContent = apps.get_model(
        app_label='document_parsing', model_name='DocumentPageContent'
    )

    document_file = DocumentFile.objects.get(
        pk=document_file_pk
    )
    logger.info(
        'Starting parsing for document file: %s', document_file
    )
    DocumentPageContent.objects.process_document_file(
        document_file=document_file
    )
