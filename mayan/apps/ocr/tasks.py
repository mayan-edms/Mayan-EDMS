import logging

from celery import chord

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import OperationalError

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .events import event_ocr_document_version_finished
from .literals import TASK_DOCUMENT_VERSION_PAGE_OCR_RETRY_DELAY
from .signals import signal_post_document_version_ocr

logger = logging.getLogger(name=__name__)


@app.task(bind=True, ignore_result=True)
def task_document_version_ocr_process(self, document_version_id, user_id=None):
    logger.info(
        'Starting OCR for document version page ID: %s', document_version_id
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(
        pk=document_version_id
    )

    try:
        document_version_page_tasks = []
        for document_version_page in document_version.pages.all():
            document_version_page_tasks.append(
                task_document_version_page_ocr_process.s(
                    document_version_page_id=document_version_page.pk,
                    user_id=user_id
                )
            )
        chord(document_version_page_tasks)(
            task_document_version_ocr_finished.s(
                document_version_id=document_version.pk, user_id=user_id
            )
        )
    except Exception as exception:
        document_version.ocr_errors.create(result=exception)
        raise


@app.task(
    bind=True, default_retry_delay=TASK_DOCUMENT_VERSION_PAGE_OCR_RETRY_DELAY
)
def task_document_version_page_ocr_process(
    self, document_version_page_id, user_id=None
):
    CachePartitionFile = apps.get_model(
        app_label='file_caching', model_name='CachePartitionFile'
    )
    DocumentVersionPageOCRContent = apps.get_model(
        app_label='ocr', model_name='DocumentVersionPageOCRContent'
    )
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )
    document_version_page = DocumentVersionPage.objects.get(
        pk=document_version_page_id
    )

    User = get_user_model()

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    try:
        DocumentVersionPageOCRContent.objects.process_document_version_page(
            document_version_page=document_version_page,
            user=user
        )
    except CachePartitionFile.DoesNotExist as exception:
        logger.info(
            'Document version page image not found. Possible cause '
            'overloaded system or cache size too small. Retrying task.',
        )
        raise self.retry(exc=exception)
    except LockError as exception:
        raise self.retry(exc=exception)
    except OperationalError as exception:
        raise self.retry(exc=exception)


@app.task(bind=True, ignore_result=True)
def task_document_version_ocr_finished(self, results, document_version_id, user_id=None):
    logger.info(
        'OCR complete for document version ID: %s', document_version_id
    )

    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    document_version = DocumentVersion.objects.get(pk=document_version_id)

    document_version.ocr_errors.all().delete()

    User = get_user_model()

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    try:
        event_ocr_document_version_finished.commit(
            action_object=document_version.document, actor=user,
            target=document_version
        )

        signal_post_document_version_ocr.send(
            sender=document_version.__class__,
            instance=document_version
        )
    except Exception as exception:
        logger.error(
            'Exception in OCR finish for document version: %d; %s',
            document_version_id, exception, exc_info=True
        )
        document_version.ocr_errors.create(result=exception)
        raise
    except OperationalError as exception:
        logger.warning(
            'Operational error in OCR finish for document version: %d; %s. '
            'Retrying.', document_version, exception
        )
        raise self.retry(exc=exception)
