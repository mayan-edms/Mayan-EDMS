from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..permissions import (
    permission_document_download, permission_document_version_revert,
    permission_document_version_view, permission_document_view,
)


def is_not_current_version(context):
    # Use the 'object' key when the document version is an object in a list,
    # such as when showing the version list view and use the 'resolved_object'
    # when the document version is the context object, such as when showing the
    # signatures list of a documern version. This can be fixed by updating
    # the navigations app object resolution logic to use 'resolved_object' even
    # for objects in a list.
    document_version = context.get('object', context['resolved_object'])
    return document_version.document.latest_version.timestamp != document_version.timestamp


link_document_version_list = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_list',
    permissions=(permission_document_version_view,),
    text=_('Versions'), view='documents:document_version_list',
)
link_document_version_download = Link(
    args='resolved_object.pk',
    icon_class_path='mayan.apps.documents.icons.icon_document_version_download',
    permissions=(permission_document_download,), text=_('Download version'),
    view='documents:document_version_download_form'
)
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
    text=_('Details'), view='documents:document_version_view'
)
link_document_version_revert = Link(
    args='object.pk', condition=is_not_current_version,
    icon_class_path='mayan.apps.documents.icons.icon_document_version_revert',
    permissions=(permission_document_version_revert,), tags='dangerous',
    text=_('Revert'), view='documents:document_version_revert',
)
