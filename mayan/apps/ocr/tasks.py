import logging

from celery import chain, chord

from django.apps import apps
from django.db import OperationalError

from mayan.apps.documents.tasks import task_document_version_page_image_generate
from mayan.celery import app

from .events import event_ocr_document_version_finish
from .literals import DO_OCR_RETRY_DELAY
from .signals import signal_post_document_version_ocr

logger = logging.getLogger(name=__name__)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_version_ocr_process(self, document_version_id):
    logger.info(
        'Starting OCR for document file page: %s', document_version_id
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(
        pk=document_version_id
    )

    try:
        page_tasks = []
        for document_version_page in document_version.pages.all():
            page_tasks.append(
                chain(
                    task_document_version_page_image_generate.s(
                        document_version_page_id=document_version_page.pk
                    ),
                    task_document_version_page_ocr_process.s(
                        document_version_page_id=document_version_page.pk
                    )
                )
            )
        chord(page_tasks)(
            task_document_version_ocr_finished.s(
                document_version_id=document_version.pk
            )
        )
    except Exception as exception:
        document_version.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'OCR operational error for document file: %d; %s. Retrying.',
            document_version_id, exception
        )
        raise self.retry(exc=exception)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_document_version_page_ocr_process(
    self, cache_filename, document_version_page_id
):
    DocumentVersionPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentVersionPageOCRContent'
    )
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )
    document_version_page = DocumentVersionPage.objects.get(
        pk=document_version_page_id
    )

    try:
        DocumentVersionPageOCRContent.objects.process_document_version_page(
            cache_filename=cache_filename,
            document_version_page=document_version_page,
        )
    except OperationalError as exception:
        raise self.retry(exc=exception)


@app.task(bind=True, ignore_result=True)
def task_document_version_ocr_finished(self, results, document_version_id):
    logger.info(
        'OCR complete for document file: %s', document_version_id
    )

    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    document_version = DocumentVersion.objects.get(pk=document_version_id)

    document_version.ocr_errors.all().delete()

    try:
        event_ocr_document_version_finish.commit(
            action_object=document_version.document,
            target=document_version
        )

        signal_post_document_version_ocr.send(
            sender=document_version.__class__,
            instance=document_version
        )
    except Exception as exception:
        logger.error(
            'Exception in OCR finish for document file: %d; %s',
            document_version_id,
            exception
        )
        document_version.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'Operational error in OCR finish for document file: %d; %s. '
            'Retrying.', document_version, exception
        )
        raise self.retry(exc=exception)
