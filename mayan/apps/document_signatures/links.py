from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY,
    PERMISSION_SIGNATURE_DELETE,
    PERMISSION_SIGNATURE_DOWNLOAD,
    PERMISSION_SIGNATURE_UPLOAD,
)


def has_embedded_signature(context):
    return DocumentVersionSignature.objects.has_embedded_signature(context['object'])


def doesnt_have_detached_signature(context):
    return DocumentVersionSignature.objects.has_detached_signature(context['object']) is False


link_document_signature_delete = Link(conditional_disable=doesnt_have_detached_signature, permissions=[PERMISSION_SIGNATURE_DELETE], text=_('Delete signature'), view='signatures:document_signature_delete', args='object.pk')
link_document_signature_download = Link(conditional_disable=doesnt_have_detached_signature, text=_('Download signature'), view='signatures:document_signature_download', args='object.pk', permissions=[PERMISSION_SIGNATURE_DOWNLOAD])
link_document_signature_upload = Link(conditional_disable=has_embedded_signature, permissions=[PERMISSION_SIGNATURE_UPLOAD], text=_('Upload signature'), view='signatures:document_signature_upload', args='object.pk')
link_document_verify = Link(permissions=[PERMISSION_DOCUMENT_VERIFY], text=_('Signatures'), view='signatures:document_verify', args='object.pk')
