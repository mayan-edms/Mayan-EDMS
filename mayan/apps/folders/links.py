from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from navigation import Link

from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_REMOVE_DOCUMENT
)

link_folder_create = Link(permissions=[PERMISSION_FOLDER_CREATE], text=_('Create folder'), view='folders:folder_create')
link_folder_list = Link(icon='fa fa-folder', text=_('Folders'), view='folders:folder_list')

link_folder_edit = Link(permissions=[PERMISSION_FOLDER_EDIT], text=_('Edit'), view='folders:folder_edit', args='object.pk')
link_folder_delete = Link(permissions=[PERMISSION_FOLDER_DELETE], text=_('Delete'), view='folders:folder_delete', args='object.pk')
link_folder_view = Link(permissions=[PERMISSION_FOLDER_VIEW], text=_('Documents'), view='folders:folder_view', args='object.pk')
link_folder_acl_list = Link(permissions=[ACLS_VIEW_ACL], text=_('ACLs'), view='folders:folder_acl_list', args='object.pk')

link_folder_document_multiple_remove = Link(permissions=[PERMISSION_FOLDER_REMOVE_DOCUMENT], text=_('Remove from folder'), view='folders:folder_document_multiple_remove', args='object.pk')
link_folder_add_document = Link(permissions=[PERMISSION_FOLDER_ADD_DOCUMENT], text=_('Add to a folder'), view='folders:folder_add_document', args='object.pk')
link_folder_add_multiple_documents = Link(text=_('Add to folder'), view='folders:folder_add_multiple_documents')
link_document_folder_list = Link(permissions=[PERMISSION_DOCUMENT_VIEW], text=_('Folders'), view='folders:document_folder_list', args='object.pk')

