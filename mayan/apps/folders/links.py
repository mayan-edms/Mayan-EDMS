from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import permission_document_view
from navigation import Link

from .permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit, permission_folder_view,
    permission_folder_remove_document
)

link_document_folder_list = Link(
    permissions=(permission_document_view,), text=_('Folders'),
    view='folders:document_folder_list', args='object.pk'
)
link_folder_add_document = Link(
    permissions=(permission_folder_add_document,), text=_('Add to a folder'),
    view='folders:folder_add_document', args='object.pk'
)
link_folder_add_multiple_documents = Link(
    text=_('Add to folder'), view='folders:folder_add_multiple_documents'
)
link_folder_create = Link(
    permissions=(permission_folder_create,), text=_('Create folder'),
    view='folders:folder_create'
)
link_folder_delete = Link(
    permissions=(permission_folder_delete,), tags='dangerous',
    text=_('Delete'), view='folders:folder_delete', args='object.pk'
)
link_folder_document_multiple_remove = Link(
    permissions=(permission_folder_remove_document,),
    text=_('Remove from folder'),
    view='folders:folder_document_multiple_remove', args='object.pk'
)
link_folder_edit = Link(
    permissions=(permission_folder_edit,), text=_('Edit'),
    view='folders:folder_edit', args='object.pk'
)
link_folder_list = Link(
    icon='fa fa-folder', text=_('Folders'), view='folders:folder_list'
)
link_folder_view = Link(
    permissions=(permission_folder_view,), text=_('Documents'),
    view='folders:folder_view', args='object.pk'
)
