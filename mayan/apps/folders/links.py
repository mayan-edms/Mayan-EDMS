from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import permission_document_view
from navigation import Link

from .permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit, permission_folder_view,
    permission_folder_remove_document
)

# Document links

link_document_folder_list = Link(
    icon='fa fa-folder', permissions=(permission_document_view,),
    text=_('Folders'), view='folders:document_folder_list',
    args='resolved_object.pk'
)
link_document_folder_remove = Link(
    args='resolved_object.pk',
    permissions=(permission_folder_remove_document,),
    text=_('Remove from folders'), view='folders:document_folder_remove'
)
link_folder_add_document = Link(
    permissions=(permission_folder_add_document,), text=_('Add to a folders'),
    view='folders:folder_add_document', args='object.pk'
)
link_folder_add_multiple_documents = Link(
    text=_('Add to folders'), view='folders:folder_add_multiple_documents'
)
link_multiple_document_folder_remove = Link(
    text=_('Remove from folders'),
    view='folders:multiple_document_folder_remove'
)

# Folder links

link_folder_create = Link(
    icon='fa fa-plus', permissions=(permission_folder_create,),
    text=_('Create folder'), view='folders:folder_create'
)
link_folder_delete = Link(
    permissions=(permission_folder_delete,), tags='dangerous',
    text=_('Delete'), view='folders:folder_delete', args='object.pk'
)
link_folder_edit = Link(
    permissions=(permission_folder_edit,), text=_('Edit'),
    view='folders:folder_edit', args='object.pk'
)
link_folder_list = Link(
    icon='fa fa-folder', text=_('All'), view='folders:folder_list'
)
link_folder_view = Link(
    permissions=(permission_folder_view,), text=_('Documents'),
    view='folders:folder_view', args='object.pk'
)
