from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)


def post_version_upload_ocr(sender, instance, **kwargs):
    logger.debug('received post_version_upload')
    logger.debug('instance pk: %s', instance.pk)
    if instance.document.document_type.ocr:
        instance.submit_for_ocr()
