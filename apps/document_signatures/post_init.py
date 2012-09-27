from __future__ import absolute_import

import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

#from django.db.models.signals import post_save
#from django.dispatch import receiver

from documents.models import Document, DocumentVersion
from navigation.api import bind_links
from django_gpg.runtime import gpg
from django_gpg.exceptions import GPGDecryptionError
from acls.api import class_permissions
from documents.settings import STORAGE_BACKEND

from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_DELETE
)
from .links import (document_signature_upload, document_signature_download,
    document_signature_delete, document_verify)

logger = logging.getLogger(__name__)


def document_pre_open_hook(descriptor, instance):
    if DocumentVersionSignature.objects.has_embedded_signature(instance.document):
        # If it has an embedded signature decrypt
        try:
            result = gpg.decrypt_file(descriptor, close_descriptor=False)
            # gpg return a string, turn it into a file like object
        except GPGDecryptionError:
            # At least return the original raw content
            descriptor.seek(0)
            return descriptor
        else:
            descriptor.close()
            return StringIO(result.data)
    else:
        # It no embedded signature pass along
        # Doing this single DB lookup avoids trying to decrypt non signed
        # files always, which could result in slow down for big non signed
        # files
        #descriptor.seek(0)
        return descriptor

    #try:
    #    result = gpg.decrypt_file(descriptor, close_descriptor=False)
    #    # gpg return a string, turn it into a file like object
    #except GPGDecryptionError:
    #    # At least return the original raw content
    #    descriptor.seek(0)
    #    return descriptor
    #else:
    #    descriptor.close()
    #    return StringIO(result.data)


def document_post_save_hook(instance):
    if not instance.pk:
        document_signature, created = DocumentVersionSignature.objects.get_or_create(
            document_version=instance.latest_version,
        )
        #DocumentVersionSignature.objects.update_signed_state(instance.document)

#@receiver(post_save, dispatch_uid='check_document_signature_state', sender=DocumentVersion)
#def check_document_signature_state(sender, instance, **kwargs):
#    if kwargs.get('created', False):
#        DocumentVersionSignature.objects.signature_state(instance.document)

bind_links([Document], [document_verify], menu_name='form_header')
bind_links(['document_verify', 'document_signature_upload', 'document_signature_download', 'document_signature_delete'], [document_signature_upload, document_signature_download, document_signature_delete], menu_name='sidebar')

DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)
DocumentVersion.register_post_save_hook(1, document_post_save_hook)

class_permissions(Document, [
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_DELETE
])

DocumentVersionSignature._meta.get_field('signature_file').storage=STORAGE_BACKEND()
