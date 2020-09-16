import logging

from celery import chain, chord

from django.apps import apps
from django.db import OperationalError, transaction

from mayan.apps.documents.tasks import task_generate_document_page_image
from mayan.celery import app

from .events import event_ocr_document_file_finish
from .literals import DO_OCR_RETRY_DELAY
from .signals import signal_post_document_file_ocr

logger = logging.getLogger(name=__name__)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_file_process(self, document_file_pk):
    logger.info('Starting OCR for document file page: %s', document_file_pk)
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    document_file = DocumentFile.objects.get(
        pk=document_file_pk
    )

    try:
        page_tasks = []
        for document_file_page in document_file.pages.all():
            page_tasks.append(
                chain(
                    task_generate_document_page_image.s(document_page_id=document_file_page.pk),
                    task_document_file_page_process_ocr.s(document_page_pk=document_file_page.pk)
                )
            )
        chord(page_tasks)(task_document_file_finished.s(document_file_pk=document_file.pk))
    except Exception as exception:
        document_file.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'OCR operational error for document file: %d; %s. Retrying.',
            document_file_pk, exception
        )
        raise self.retry(exc=exception)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_file_page_process_ocr(self, cache_filename, document_page_pk):
    DocumentPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentPageOCRContent'
    )
    DocumentPage = apps.get_model(
        app_label='documents', model_name='DocumentPage'
    )
    document_page = DocumentPage.objects.get(pk=document_page_pk)

    try:
        DocumentPageOCRContent.objects.process_document_page(
            cache_filename=cache_filename, document_page=document_page,
        )
    except OperationalError as exception:
        raise self.retry(exc=exception)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_file_finished(self, results, document_file_pk):
    logger.info(
        'OCR complete for document file: %s', document_file_pk
    )

    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )
    document_file = DocumentFile.objects.get(pk=document_file_pk)

    document_file.ocr_errors.all().delete()

    try:
        with transaction.atomic():
            event_ocr_document_file_finish.commit(
                action_object=document_file.document,
                target=document_file
            )

            transaction.on_commit(
                lambda: signal_post_document_file_ocr.send(
                    sender=document_file.__class__,
                    instance=document_file
                )
            )
    except Exception as exception:
        logger.error(
            'Exception in OCR finish for document file: %d; %s', document_file_pk,
            exception
        )
        document_file.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'Operational error in OCR finish for document file: %d; %s. Retrying.',
            document_file, exception
        )
        raise self.retry(exc=exception)
