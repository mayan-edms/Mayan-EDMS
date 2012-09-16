from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD, PERMISSION_SIGNATURE_DELETE
)
from .icons import (icon_document_signature_upload, icon_document_signature_download,
    icon_document_signature_delete, icon_document_verify)


def has_embedded_signature(context):
    return DocumentVersionSignature.objects.has_embedded_signature(context['object'])


def doesnt_have_detached_signature(context):
    return DocumentVersionSignature.objects.has_detached_signature(context['object']) == False


document_signature_upload = Link(text=_(u'upload signature'), view='document_signature_upload', args='object.pk', icon=icon_document_signature_upload, permissions=[PERMISSION_SIGNATURE_UPLOAD], conditional_disable=has_embedded_signature)
document_signature_download = Link(text=_(u'download signature'), view='document_signature_download', args='object.pk', icon=icon_document_signature_download, permissions=[PERMISSION_SIGNATURE_DOWNLOAD], conditional_disable=doesnt_have_detached_signature)
document_signature_delete = Link(text=_(u'delete signature'), view='document_signature_delete', args='object.pk', icon=icon_document_signature_delete, permissions=[PERMISSION_SIGNATURE_DELETE], conditional_disable=doesnt_have_detached_signature)
document_verify = Link(text=_(u'signatures'), view='document_verify', args='object.pk', icon=icon_document_verify, permissions=[PERMISSION_DOCUMENT_VERIFY])
