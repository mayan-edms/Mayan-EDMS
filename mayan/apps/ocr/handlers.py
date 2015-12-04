from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

from .models import DocumentTypeSettings
from .settings import setting_auto_ocr


def post_version_upload_ocr(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr_settings.auto_ocr:
        instance.submit_for_ocr()


def initialize_new_ocr_settings(sender, instance, **kwargs):
    if kwargs['created']:
        DocumentTypeSettings.objects.create(
            document_type=instance, auto_ocr=setting_auto_ocr.value
        )
