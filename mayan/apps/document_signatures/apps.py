from __future__ import unicode_literals

import io
import logging

from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from common import MayanAppConfig, menu_facet, menu_sidebar
from django_gpg.exceptions import GPGDecryptionError
from django_gpg.runtime import gpg
from documents.models import Document, DocumentVersion

from .links import (
    link_document_signature_delete, link_document_signature_download,
    link_document_signature_upload, link_document_verify
)
from .models import DocumentVersionSignature
from .permissions import (
    permission_document_verify, permission_signature_delete,
    permission_signature_download, permission_signature_upload
)

logger = logging.getLogger(__name__)


def document_pre_open_hook(descriptor, instance):
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

    try:
        document_signature = DocumentVersionSignature.objects.get(
            document_version=instance
        )
    except DocumentVersionSignature.DoesNotExist:
        document_signature = DocumentVersionSignature.objects.create(
            document_version=instance
        )
        document_signature.check_for_embedded_signature()


class DocumentSignaturesApp(MayanAppConfig):
    app_namespace = 'signatures'
    app_url = 'signatures'
    name = 'document_signatures'
    test = True
    verbose_name = _('Document signatures')

    def ready(self):
        super(DocumentSignaturesApp, self).ready()

        DocumentVersion.register_post_save_hook(
            1, document_version_post_save_hook
        )
        DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_verify, permission_signature_delete,
                permission_signature_download, permission_signature_upload,
            )
        )

        menu_facet.bind_links(
            links=(link_document_verify,), sources=(Document,)
        )
        menu_sidebar.bind_links(
            links=(
                link_document_signature_upload,
                link_document_signature_download,
                link_document_signature_delete
            ), sources=(
                'signatures:document_verify',
                'signatures:document_signature_upload',
                'signatures:document_signature_download',
                'signatures:document_signature_delete'
            )
        )
