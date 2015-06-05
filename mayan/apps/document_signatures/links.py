from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_DELETE,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_UPLOAD,
)


def can_upload_detached_signature(context):
    return not DocumentVersionSignature.objects.has_detached_signature(context['object'].latest_version) and not DocumentVersionSignature.objects.has_embedded_signature(context['object'].latest_version)


def can_delete_detached_signature(context):
    return DocumentVersionSignature.objects.has_detached_signature(context['object'].latest_version)


link_document_signature_delete = Link(condition=can_delete_detached_signature, permissions=[PERMISSION_SIGNATURE_DELETE], tags='dangerous', text=_('Delete signature'), view='signatures:document_signature_delete', args='object.pk')
link_document_signature_download = Link(condition=can_delete_detached_signature, text=_('Download signature'), view='signatures:document_signature_download', args='object.pk', permissions=[PERMISSION_SIGNATURE_DOWNLOAD])
link_document_signature_upload = Link(condition=can_upload_detached_signature, permissions=[PERMISSION_SIGNATURE_UPLOAD], text=_('Upload signature'), view='signatures:document_signature_upload', args='object.pk')
link_document_verify = Link(permissions=[PERMISSION_DOCUMENT_VERIFY], text=_('Signatures'), view='signatures:document_verify', args='object.pk')
