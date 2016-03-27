from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
)


def is_detached_signature(context):
    SignatureBaseModel = apps.get_model(
        app_label='document_signatures', model_name='SignatureBaseModel'
    )

    return SignatureBaseModel.objects.select_subclasses().get(
        pk=context['object'].pk
    ).is_detached


link_document_version_signature_delete = Link(
    condition=is_detached_signature,
    #permissions=(permission_document_version_signature_delete,),
    tags='dangerous', text=_('Delete'),
    view='signatures:document_version_signature_delete',
    args='resolved_object.pk'
)
link_document_version_signature_details = Link(
    #permissions=(permission_document_version_signature_view,),
    text=_('Details'),
    view='signatures:document_version_signature_details',
    args='resolved_object.pk'
)
link_document_version_signature_list = Link(
    #permissions=(permission_document_version_signature_view,),
    text=_('Signature list'),
    view='signatures:document_version_signature_list',
    args='resolved_object.pk'
)
link_document_version_signature_download = Link(
    condition=is_detached_signature,
    text=_('Download'),
    view='signatures:document_version_signature_download', args='resolved_object.pk',
    #permissions=(permission_document_version_signature_download,)
)
link_document_version_signature_upload = Link(
    #permissions=(permission_document_version_signature_upload,),
    text=_('Upload signature'),
    view='signatures:document_version_signature_upload',
    args='resolved_object.pk'
)
