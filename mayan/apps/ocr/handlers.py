import logging

from django.apps import apps

from .settings import setting_auto_ocr

logger = logging.getLogger(name=__name__)


def handler_initialize_new_ocr_settings(sender, instance, **kwargs):
    DocumentTypeOCRSettings = apps.get_model(
        app_label='ocr', model_name='DocumentTypeOCRSettings'
    )

    if kwargs['created']:
        DocumentTypeOCRSettings.objects.create(
            document_type=instance, auto_ocr=setting_auto_ocr.value
        )


def handler_ocr_document_version(sender, instance, **kwargs):
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr_settings.auto_ocr:
        instance.submit_for_ocr()
