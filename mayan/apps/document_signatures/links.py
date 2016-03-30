from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
    permission_document_version_signature_verify,
    permission_document_version_signature_view
)


def is_detached_signature(context):
    SignatureBaseModel = apps.get_model(
        app_label='document_signatures', model_name='SignatureBaseModel'
    )

    return SignatureBaseModel.objects.select_subclasses().get(
        pk=context['object'].pk
    ).is_detached


link_all_document_version_signature_verify = Link(
    permissions=(permission_document_version_signature_verify,),
    text=_('Verify all documents'),
    view='signatures:all_document_version_signature_verify',
)
link_document_version_signature_delete = Link(
    args='resolved_object.pk', condition=is_detached_signature,
    permissions=(permission_document_version_signature_delete,),
    permissions_related='document_version.document', tags='dangerous',
    text=_('Delete'), view='signatures:document_version_signature_delete',
)
link_document_version_signature_details = Link(
    args='resolved_object.pk',
    permissions=(permission_document_version_signature_view,),
    permissions_related='document_version.document', text=_('Details'),
    view='signatures:document_version_signature_details',
)
link_document_version_signature_list = Link(
    args='resolved_object.pk',
    permissions=(permission_document_version_signature_view,),
    text=_('Signature list'),
    view='signatures:document_version_signature_list',
)
link_document_version_signature_download = Link(
    args='resolved_object.pk', condition=is_detached_signature,
    permissions=(permission_document_version_signature_download,),
    permissions_related='document_version.document', text=_('Download'),
    view='signatures:document_version_signature_download',
)
link_document_version_signature_upload = Link(
    args='resolved_object.pk',
    permissions=(permission_document_version_signature_upload,),
    text=_('Upload signature'),
    view='signatures:document_version_signature_upload',
)
