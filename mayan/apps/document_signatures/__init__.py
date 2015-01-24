from __future__ import unicode_literals

import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from acls.api import class_permissions
from django_gpg.exceptions import GPGDecryptionError
from django_gpg.runtime import gpg
from documents.models import Document, DocumentVersion
from navigation.api import register_links

from .links import (
    document_signature_delete, document_signature_download,
    document_signature_upload, document_verify
)
from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_DELETE,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_UPLOAD
)

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
        return descriptor


def document_post_save_hook(instance):
    if not instance.pk:
        document_signature, created = DocumentVersionSignature.objects.get_or_create(
            document_version=instance.latest_version,
        )


register_links(Document, [document_verify], menu_name='form_header')
register_links(['signatures:document_verify', 'signatures:document_signature_upload', 'signatures:document_signature_download', 'signatures:document_signature_delete'], [document_signature_upload, document_signature_download, document_signature_delete], menu_name='sidebar')

DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)
DocumentVersion.register_post_save_hook(1, document_post_save_hook)

class_permissions(Document, [
    PERMISSION_DOCUMENT_VERIFY,
    PERMISSION_SIGNATURE_DELETE,
    PERMISSION_SIGNATURE_DOWNLOAD,
    PERMISSION_SIGNATURE_UPLOAD,
])
