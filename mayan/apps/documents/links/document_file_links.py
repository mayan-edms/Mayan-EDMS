from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_view, permission_document_view,
)


link_document_file_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_delete',
    permissions=(permission_document_file_delete,), tags='dangerous',
    text=_('Delete'), view='documents:document_file_delete',
)
link_document_file_download = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_download',
    permissions=(permission_document_file_download,), text=_('Download file'),
    view='documents:document_file_download_form'
)
link_document_file_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_list',
    permissions=(permission_document_file_view,),
    text=_('Files'), view='documents:document_file_list',
)
link_document_file_properties = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_properties',
    permissions=(permission_document_file_view,),
    text=_('Properties'), view='documents:document_file_properties',
)
link_document_file_return_document = Link(
    args='resolved_object.document.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_return_document',
    permissions=(permission_document_view,), text=_('Document'),
    view='documents:document_preview',
)
link_document_file_return_list = Link(
    args='resolved_object.document.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_return_list',
    permissions=(permission_document_file_view,), text=_('Files'),
    view='documents:document_file_list',
)
link_document_file_view = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_view',
    permissions=(permission_document_file_view,),
    text=_('Preview'), view='documents:document_file_view'
)
