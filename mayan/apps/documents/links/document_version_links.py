from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import (
    permission_document_version_delete, permission_document_version_view,
    permission_document_view,
)


link_document_version_delete = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_delete',
    permissions=(permission_document_version_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_version_delete',
)
link_document_version_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_list',
    permissions=(permission_document_version_view,),
    text=_('Versions'), view='documents:document_version_list',
)
#link_document_version_download = Link(
#    args='resolved_object.pk',
#    icon_class_path='mayan.apps.documents.icons.icon_document_version_download',
#    permissions=(permission_document_file_download,), text=_('Download version'),
#    view='documents:document_version_download_form'
#)
link_document_version_return_document = Link(
    args='resolved_object.document.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_return_document',
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview',
)
link_document_version_return_list = Link(
    args='resolved_object.document.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_return_list',
    permissions=(permission_document_version_view,), text=_('Versions'),
    view='documents:document_version_list',
)
link_document_version_view = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_view',
    permissions=(permission_document_version_view,),
    text=_('Preview'), view='documents:document_version_view'
)
