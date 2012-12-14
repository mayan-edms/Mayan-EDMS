from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.permissions import ACLS_VIEW_ACL

from .permissions import (PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_ADD_DOCUMENT)
from .icons import (icon_folders, icon_folder_create, icon_folder_edit,
    icon_folder_delete, icon_folder_view, icon_folder_add_document,
    icon_document_folder_list, icon_folder_acls)
    
folder_list = Link(text=_(u'folder list'), view='folder_list', icon=icon_folders)
folder_create = Link(text=_('create folder'), view='folder_create', icon=icon_folder_create, permissions=[PERMISSION_FOLDER_CREATE])
folder_edit = Link(text=_('edit'), view='folder_edit', args='object.pk', icon=icon_folder_edit, permissions=[PERMISSION_FOLDER_EDIT])
folder_delete = Link(text=_('delete'), view='folder_delete', args='object.pk', icon=icon_folder_delete, permissions=[PERMISSION_FOLDER_DELETE])
folder_document_multiple_remove = Link(text=_('remove from folder'), view='folder_document_multiple_remove', args='object.pk', icon=icon_folder_delete, permissions=[PERMISSION_FOLDER_REMOVE_DOCUMENT])
folder_view = Link(text=_(u'folder documents'), view='folder_view', args='object.pk', icon=icon_folder_view, permissions=[PERMISSION_FOLDER_VIEW])
folder_add_document = Link(text=_('add to a folder'), view='folder_add_document', args='object.pk', icon=icon_folder_add_document, permissions=[PERMISSION_FOLDER_ADD_DOCUMENT])
folder_add_multiple_documents = Link(text=_('add to folder'), view='folder_add_multiple_documents', icon=icon_folder_add_document)
document_folder_list = Link(text=_(u'folders'), view='document_folder_list', args='object.pk', icon=icon_document_folder_list, permissions=[PERMISSION_DOCUMENT_VIEW], children_view_regex=[r'folder'])

folder_acl_list = Link(text=_(u'ACLs'), view='folder_acl_list', args='object.pk', icon=icon_folder_acls, permissions=[ACLS_VIEW_ACL])
menu_link = Link(text=_('folders'), icon=icon_folder_view, view='folder_list', children_views=['folder_list', 'folder_create', 'folder_edit', 'folder_delete', 'folder_view', 'folder_document_multiple_remove'])
