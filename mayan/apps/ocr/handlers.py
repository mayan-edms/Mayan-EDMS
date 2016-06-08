from __future__ import unicode_literals

import logging

from django.db.models import get_model

from .settings import setting_auto_ocr

logger = logging.getLogger(__name__)


def post_version_upload_ocr(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr_settings.auto_ocr:
        instance.submit_for_ocr()


def initialize_new_ocr_settings(sender, instance, **kwargs):
    DocumentTypeSettings = get_model('ocr', 'DocumentTypeSettings')

    if kwargs['created']:
        DocumentTypeSettings.on_organization.create(
            document_type=instance, auto_ocr=setting_auto_ocr.value
        )
