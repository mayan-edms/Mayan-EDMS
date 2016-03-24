from __future__ import unicode_literals

import io
import logging

from django.apps import apps
from django_gpg.exceptions import DecryptionError

logger = logging.getLogger(__name__)


def document_pre_open_hook(file_object, instance):
    logger.debug('instance: %s', instance)

    DocumentVersionSignature = apps.get_model(
        app_label='document_signatures', model_name='DocumentVersionSignature'
    )

    Key = apps.get_model(
        app_label='django_gpg', model_name='Key'
    )

    if DocumentVersionSignature.objects.has_embedded_signature(document_version=instance):
        # If it has an embedded signature, decrypt
        try:
            result = Key.objects.decrypt_file(file_object=file_object)
            # gpg return a string, turn it into a file like object
        except DecryptionError:
            # At least return the original raw content
            file_object.seek(0)
            return file_object
        else:
            file_object.close()
            return io.BytesIO(result)
    else:
        return file_object


def document_version_post_save_hook(instance):
    logger.debug('instance: %s', instance)

    DocumentVersionSignature = apps.get_model(
        app_label='document_signatures', model_name='DocumentVersionSignature'
    )

    try:
        document_signature = DocumentVersionSignature.objects.get(
            document_version=instance
        )
    except DocumentVersionSignature.DoesNotExist:
        document_signature = DocumentVersionSignature.objects.create(
            document_version=instance
        )
        document_signature.check_for_embedded_signature()
