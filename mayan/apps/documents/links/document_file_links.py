from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import (
    permission_document_download, permission_document_file_revert,
    permission_document_file_view, permission_document_view,
)


def is_not_current_file(context):
    # Use the 'object' key when the document file is an object in a list,
    # such as when showing the file list view and use the 'resolved_object'
    # when the document file is the context object, such as when showing the
    # signatures list of a documern file. This can be fixed by updating
    # the navigations app object resolution logic to use 'resolved_object' even
    # for objects in a list.
    document_file = context.get('object', context['resolved_object'])
    return document_file.document.latest_file.timestamp != document_file.timestamp


link_document_file_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_list',
    permissions=(permission_document_file_view,),
    text=_('Files'), view='documents:document_file_list',
)
link_document_file_download = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_file_download',
    permissions=(permission_document_download,), text=_('Download file'),
    view='documents:document_file_download_form'
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
link_document_file_revert = Link(
    args='object.pk', condition=is_not_current_file,
    icon_class_path='mayan.apps.documents.icons.icon_document_file_revert',
    permissions=(permission_document_file_revert,), tags='dangerous',
    text=_('Revert'), view='documents:document_file_revert',
)
