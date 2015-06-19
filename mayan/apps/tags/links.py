from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from navigation import Link

from .permissions import (
    PERMISSION_TAG_ATTACH, PERMISSION_TAG_CREATE, PERMISSION_TAG_DELETE,
    PERMISSION_TAG_EDIT, PERMISSION_TAG_REMOVE
)


link_multiple_documents_tag_remove = Link(text=_('Remove tag'), view='tags:multiple_documents_selection_tag_remove')
link_multiple_documents_attach_tag = Link(text=_('Attach tag'), view='tags:multiple_documents_tag_attach')
link_single_document_multiple_tag_remove = Link(permissions=[PERMISSION_TAG_REMOVE], text=_('Remove tags'), view='tags:single_document_multiple_tag_remove', args='document.id')
link_tag_acl_list = Link(permissions=[ACLS_VIEW_ACL], text=_('ACLs'), view='tags:tag_acl_list', args='object.pk')
link_tag_attach = Link(permissions=[PERMISSION_TAG_ATTACH], text=_('Attach tag'), view='tags:tag_attach', args='object.pk')
link_tag_create = Link(permissions=[PERMISSION_TAG_CREATE], text=_('Create new tag'), view='tags:tag_create')
link_tag_delete = Link(permissions=[PERMISSION_TAG_DELETE], tags='dangerous', text=_('Delete'), view='tags:tag_delete', args='object.id')
link_tag_edit = Link(permissions=[PERMISSION_TAG_EDIT], text=_('Edit'), view='tags:tag_edit', args='object.id')
link_tag_document_list = Link(permissions=[PERMISSION_TAG_REMOVE, PERMISSION_TAG_ATTACH], text=_('Tags'), view='tags:document_tags', args='object.pk')
link_tag_list = Link(icon='fa fa-tag', text=_('Tags'), view='tags:tag_list')
link_tag_multiple_delete = Link(permissions=[PERMISSION_TAG_DELETE], text=_('Delete'), view='tags:tag_multiple_delete')
link_tag_tagged_item_list = Link(text=('Documents'), view='tags:tag_tagged_item_list', args='object.id')
