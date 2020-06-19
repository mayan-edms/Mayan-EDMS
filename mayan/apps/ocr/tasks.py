import logging

from celery import chain, chord

from django.apps import apps
from django.db import OperationalError, transaction

from mayan.apps.documents.tasks import task_generate_document_page_image
from mayan.celery import app

from .events import event_ocr_document_version_finish
from .literals import DO_OCR_RETRY_DELAY
from .signals import signal_post_document_version_ocr

logger = logging.getLogger(name=__name__)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_version_process(self, document_version_pk):
    logger.info('Starting OCR for document version page: %s', document_version_pk)
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(
        pk=document_version_pk
    )

    try:
        page_tasks = []
        for document_version_page in document_version.pages.all():
            page_tasks.append(
                chain(
                    task_generate_document_page_image.s(document_page_id=document_version_page.pk),
                    task_document_version_page_process_ocr.s(document_page_pk=document_version_page.pk)
                )
            )
        chord(page_tasks)(task_document_version_finished.s(document_version_pk=document_version.pk))
    except Exception as exception:
        document_version.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'OCR operational error for document version: %d; %s. Retrying.',
            document_version_pk, exception
        )
        raise self.retry(exc=exception)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_version_page_process_ocr(self, cache_filename, document_page_pk):
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
def task_document_version_finished(self, results, document_version_pk):
    logger.info(
        'OCR complete for document version: %s', document_version_pk
    )

    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    document_version = DocumentVersion.objects.get(pk=document_version_pk)

    document_version.ocr_errors.all().delete()

    try:
        with transaction.atomic():
            event_ocr_document_version_finish.commit(
                action_object=document_version.document,
                target=document_version
            )

            transaction.on_commit(
                lambda: signal_post_document_version_ocr.send(
                    sender=document_version.__class__,
                    instance=document_version
                )
            )
    except Exception as exception:
        logger.error(
            'Exception in OCR finish for document version: %d; %s', document_version_pk,
            exception
        )
        document_version.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'Operational error in OCR finish for document version: %d; %s. Retrying.',
            document_version, exception
        )
        raise self.retry(exc=exception)
