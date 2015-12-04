from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .models import DocumentVersionSignature
from .permissions import (
    permission_document_verify, permission_signature_delete,
    permission_signature_download, permission_signature_upload,
)


def can_upload_detached_signature(context):
    return not DocumentVersionSignature.objects.has_detached_signature(
        context['object'].latest_version
    ) and not DocumentVersionSignature.objects.has_embedded_signature(
        context['object'].latest_version
    )


def can_delete_detached_signature(context):
    return DocumentVersionSignature.objects.has_detached_signature(
        context['object'].latest_version
    )


link_document_signature_delete = Link(
    condition=can_delete_detached_signature,
    permissions=(permission_signature_delete,), tags='dangerous',
    text=_('Delete signature'), view='signatures:document_signature_delete',
    args='object.pk'
)
link_document_signature_download = Link(
    condition=can_delete_detached_signature, text=_('Download signature'),
    view='signatures:document_signature_download', args='object.pk',
    permissions=(permission_signature_download,)
)
link_document_signature_upload = Link(
    condition=can_upload_detached_signature,
    permissions=(permission_signature_upload,), text=_('Upload signature'),
    view='signatures:document_signature_upload', args='object.pk'
)
link_document_verify = Link(
    permissions=(permission_document_verify,), text=_('Signatures'),
    view='signatures:document_verify', args='object.pk'
)
