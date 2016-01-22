from __future__ import unicode_literals

import io
import logging

from django_gpg.exceptions import GPGDecryptionError
from django_gpg.runtime import gpg

logger = logging.getLogger(__name__)


def document_pre_open_hook(descriptor, instance):
    from .models import DocumentVersionSignature

    if DocumentVersionSignature.objects.has_embedded_signature(document_version=instance):
        # If it has an embedded signature, decrypt
        try:
            result = gpg.decrypt_file(descriptor, close_descriptor=False)
            # gpg return a string, turn it into a file like object
        except GPGDecryptionError:
            # At least return the original raw content
            descriptor.seek(0)
            return descriptor
        else:
            descriptor.close()
            return io.BytesIO(result.data)
    else:
        return descriptor


def document_version_post_save_hook(instance):
    logger.debug('instance: %s', instance)
    from .models import DocumentVersionSignature

    try:
        document_signature = DocumentVersionSignature.objects.get(
            document_version=instance
        )
    except DocumentVersionSignature.DoesNotExist:
        document_signature = DocumentVersionSignature.objects.create(
            document_version=instance
        )
        document_signature.check_for_embedded_signature()
