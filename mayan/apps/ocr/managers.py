from __future__ import unicode_literals

import logging
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.db import models, transaction

from mayan.apps.documents.literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from mayan.apps.documents.tasks import task_generate_document_page_image

from .events import (
    event_ocr_document_content_deleted, event_ocr_document_version_finish
)
from .runtime import ocr_backend
from .signals import post_document_version_ocr

logger = logging.getLogger(__name__)


class DocumentPageOCRContentManager(models.Manager):
    def delete_content_for(self, document, user=None):
        with transaction.atomic():
            for document_page in document.pages.all():
                self.filter(document_page=document_page).delete()

            event_ocr_document_content_deleted.commit(
                actor=user, target=document
            )

    def process_document_page(self, document_page):
        logger.info(
            'Processing page: %d of document version: %s',
            document_page.page_number, document_page.document_version
        )

        DocumentPageOCRContent = apps.get_model(
            app_label='ocr', model_name='DocumentPageOCRContent'
        )

        task = task_generate_document_page_image.apply_async(
            kwargs=dict(
                document_page_id=document_page.pk
            )
        )

        cache_filename = task.get(timeout=DOCUMENT_IMAGE_TASK_TIMEOUT, disable_sync_subtasks=False)

        with document_page.cache_partition.get_file(filename=cache_filename).open() as file_object:
            document_page_content, created = DocumentPageOCRContent.objects.get_or_create(
                document_page=document_page
            )
            document_page_content.content = ocr_backend.execute(
                file_object=file_object,
                language=document_page.document.language
            )
            document_page_content.save()

        logger.info(
            'Finished processing page: %d of document version: %s',
            document_page.page_number, document_page.document_version
        )

    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        try:
            for document_page in document_version.pages.all():
                self.process_document_page(document_page=document_page)
        except Exception as exception:
            logger.error(
                'OCR error for document version: %d; %s', document_version.pk,
                exception
            )

            if settings.DEBUG:
                result = []
                type, value, tb = sys.exc_info()
                result.append('%s: %s' % (type.__name__, value))
                result.extend(traceback.format_tb(tb))
                document_version.ocr_errors.create(
                    result='\n'.join(result)
                )
            else:
                document_version.ocr_errors.create(result=exception)
        else:
            logger.info(
                'OCR complete for document version: %s', document_version
            )
            document_version.ocr_errors.all().delete()

            event_ocr_document_version_finish.commit(
                action_object=document_version.document,
                target=document_version
            )

            post_document_version_ocr.send(
                sender=document_version.__class__, instance=document_version
            )


class DocumentTypeSettingsManager(models.Manager):
    def get_by_natural_key(self, document_type_natural_key):
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        try:
            document_type = DocumentType.objects.get_by_natural_key(document_type_natural_key)
        except DocumentType.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document_type__pk=document_type.pk)
