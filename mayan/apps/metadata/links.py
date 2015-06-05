from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_TYPE_EDIT
from navigation import Link

from .permissions import (
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_EDIT, PERMISSION_METADATA_TYPE_VIEW
)

link_documents_missing_required_metadata = Link(icon='fa fa-edit', text=_('Missing metadata'), view='metadata:documents_missing_required_metadata')
link_metadata_add = Link(permissions=[PERMISSION_METADATA_DOCUMENT_ADD], text=_('Add metadata'), view='metadata:metadata_add', args='object.pk')
link_metadata_edit = Link(permissions=[PERMISSION_METADATA_DOCUMENT_EDIT], text=_('Edit metadata'), view='metadata:metadata_edit', args='object.pk')
link_metadata_multiple_add = Link(permissions=[PERMISSION_METADATA_DOCUMENT_ADD], text=_('Add metadata'), view='metadata:metadata_multiple_add')
link_metadata_multiple_edit = Link(permissions=[PERMISSION_METADATA_DOCUMENT_EDIT], text=_('Edit metadata'), view='metadata:metadata_multiple_edit')
link_metadata_multiple_remove = Link(permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE], text=_('Remove metadata'), view='metadata:metadata_multiple_remove')
link_metadata_remove = Link(permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE], text=_('Remove metadata'), view='metadata:metadata_remove', args='object.pk')
link_metadata_view = Link(permissions=[PERMISSION_METADATA_DOCUMENT_VIEW], text=_('Metadata'), view='metadata:metadata_view', args='object.pk')
link_setup_document_type_metadata = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], text=_('Optional metadata'), view='metadata:setup_document_type_metadata', args='resolved_object.pk')
link_setup_document_type_metadata_required = Link(permissions=[PERMISSION_DOCUMENT_TYPE_EDIT], text=_('Required metadata'), view='metadata:setup_document_type_metadata_required', args='resolved_object.pk')
link_setup_metadata_type_create = Link(permissions=[PERMISSION_METADATA_TYPE_CREATE], text=_('Create new'), view='metadata:setup_metadata_type_create')
link_setup_metadata_type_delete = Link(permissions=[PERMISSION_METADATA_TYPE_DELETE], tags='dangerous', text=_('Delete'), view='metadata:setup_metadata_type_delete', args='object.pk')
link_setup_metadata_type_edit = Link(permissions=[PERMISSION_METADATA_TYPE_EDIT], text=_('Edit'), view='metadata:setup_metadata_type_edit', args='object.pk')
link_setup_metadata_type_list = Link(icon='fa fa-list', permissions=[PERMISSION_METADATA_TYPE_VIEW], text=_('Metadata types'), view='metadata:setup_metadata_type_list')
