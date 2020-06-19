import logging

from django.apps import apps
from django.db import models, transaction

from .classes import OCRBackendBase
from .events import event_ocr_document_content_deleted

logger = logging.getLogger(name=__name__)


class DocumentPageOCRContentManager(models.Manager):
    def delete_content_for(self, document, user=None):
        with transaction.atomic():
            for document_page in document.pages.all():
                self.filter(document_page=document_page).delete()

            event_ocr_document_content_deleted.commit(
                actor=user, target=document
            )

    def process_document_page(self, cache_filename, document_page):
        logger.info(
            'Processing page: %d of document version: %s',
            document_page.page_number, document_page.document_version
        )

        DocumentPageOCRContent = apps.get_model(
            app_label='ocr', model_name='DocumentPageOCRContent'
        )

        try:
            with document_page.cache_partition.get_file(filename=cache_filename).open() as file_object:
                ocr_content = OCRBackendBase.get_instance().execute(
                    file_object=file_object,
                    language=document_page.document.language
                )
                DocumentPageOCRContent.objects.update_or_create(
                    document_page=document_page, defaults={
                        'content': ocr_content
                    }
                )
        except Exception as exception:
            logger.error(
                'OCR error for document page: %d; %s', document_page.pk,
                exception
            )
            raise
        else:
            logger.info(
                'Finished processing page: %d of document version: %s',
                document_page.page_number, document_page.document_version
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
