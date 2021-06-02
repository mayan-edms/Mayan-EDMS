import logging

from django.apps import apps
from django.db import models, transaction

from mayan.apps.documents.literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from mayan.apps.lock_manager.backends.base import LockingBackend

from .classes import OCRBackendBase
from .events import event_ocr_document_version_content_deleted

logger = logging.getLogger(name=__name__)


class DocumentVersionPageOCRContentManager(models.Manager):
    def delete_content_for(self, document_version, user=None):
        with transaction.atomic():
            for document_version_page in document_version.pages.all():
                self.filter(
                    document_version_page=document_version_page
                ).delete()

            event_ocr_document_version_content_deleted.commit(
                actor=user, action_object=document_version.document,
                target=document_version
            )

    def process_document_version_page(
        self, document_version_page, user=None
    ):
        logger.info(
            'Processing page: %d of document version: %s',
            document_version_page.page_number,
            document_version_page.document_version
        )

        DocumentVersionPageOCRContent = apps.get_model(
            app_label='ocr', model_name='DocumentVersionPageOCRContent'
        )

        lock_name = document_version_page.get_lock_name(user=user)

        try:
            document_version_page_lock = LockingBackend.get_backend().acquire_lock(
                name=lock_name, timeout=DOCUMENT_IMAGE_TASK_TIMEOUT * 2

            )
        except Exception:
            raise
        else:
            try:
                cache_filename = document_version_page.generate_image(
                    _acquire_lock=False, user=user
                )

                with document_version_page.cache_partition.get_file(filename=cache_filename).open() as file_object:
                    ocr_content = OCRBackendBase.get_instance().execute(
                        file_object=file_object,
                        language=document_version_page.document_version.document.language
                    )
                    DocumentVersionPageOCRContent.objects.update_or_create(
                        document_version_page=document_version_page, defaults={
                            'content': ocr_content
                        }
                    )
            except Exception as exception:
                logger.error(
                    'OCR error for document version page: %d; %s',
                    document_version_page.pk, exception, exc_info=True
                )
                raise
            else:
                logger.info(
                    'Finished processing page: %d of document version: %s',
                    document_version_page.page_number,
                    document_version_page.document_version
                )
            finally:
                document_version_page_lock.release()


class DocumentTypeSettingsManager(models.Manager):
    def get_by_natural_key(self, document_type_natural_key):
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        try:
            document_type = DocumentType.objects.get_by_natural_key(
                document_type_natural_key
            )
        except DocumentType.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document_type__pk=document_type.pk)
