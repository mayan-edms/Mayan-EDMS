from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_document_file_all_signature_refresh,
    icon_document_file_all_signature_verify,
    icon_document_file_signature_delete,
    icon_document_file_signature_detached_create,
    icon_document_file_signature_details,
    icon_document_file_signature_download,
    icon_document_file_signature_embedded_create,
    icon_document_file_signature_list, icon_document_file_signature_upload,
)
from .permissions import (
    permission_document_file_sign_detached,
    permission_document_file_sign_embedded,
    permission_document_file_signature_delete,
    permission_document_file_signature_download,
    permission_document_file_signature_upload,
    permission_document_file_signature_verify,
    permission_document_file_signature_view
)


def is_detached_signature(context):
    SignatureBaseModel = apps.get_model(
        app_label='document_signatures', model_name='SignatureBaseModel'
    )

    return SignatureBaseModel.objects.select_subclasses().get(
        pk=context['object'].pk
    ).is_detached


link_document_file_all_signature_refresh = Link(
    icon=icon_document_file_all_signature_refresh,
    permissions=(permission_document_file_signature_verify,),
    text=_('Refresh all signatures'),
    view='signatures:all_document_file_signature_refresh',
)
link_document_file_all_signature_verify = Link(
    icon=icon_document_file_all_signature_verify,
    permissions=(permission_document_file_signature_verify,),
    text=_('Verify all documents'),
    view='signatures:all_document_file_signature_verify',
)
link_document_file_signature_delete = Link(
    args='resolved_object.pk', condition=is_detached_signature,
    icon=icon_document_file_signature_delete,
    permissions=(permission_document_file_signature_delete,),
    tags='dangerous', text=_('Delete'),
    view='signatures:document_file_signature_delete',
)
link_document_file_signature_detached_create = Link(
    args='resolved_object.pk',
    icon=icon_document_file_signature_detached_create,
    permissions=(permission_document_file_sign_detached,),
    text=_('Sign detached'),
    view='signatures:document_file_signature_detached_create'
)
link_document_file_signature_details = Link(
    args='resolved_object.pk',
    icon=icon_document_file_signature_details,
    permissions=(permission_document_file_signature_view,),
    text=_('Details'), view='signatures:document_file_signature_details',
)
link_document_file_signature_download = Link(
    args='resolved_object.pk',
    icon=icon_document_file_signature_download,
    condition=is_detached_signature,
    permissions=(permission_document_file_signature_download,),
    text=_('Download'), view='signatures:document_file_signature_download'
)
link_document_file_signature_embedded_create = Link(
    args='resolved_object.pk',
    icon=icon_document_file_signature_embedded_create,
    permissions=(permission_document_file_sign_embedded,),
    text=_('Sign embedded'),
    view='signatures:document_file_signature_embedded_create'
)
link_document_file_signature_list = Link(
    args='resolved_object.pk', icon=icon_document_file_signature_list,
    permissions=(permission_document_file_signature_view,),
    text=_('Signatures'), view='signatures:document_file_signature_list'
)
link_document_file_signature_upload = Link(
    args='resolved_object.pk',
    icon=icon_document_file_signature_upload,
    permissions=(permission_document_file_signature_upload,),
    text=_('Upload signature'),
    view='signatures:document_file_signature_upload'
)
