from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL

from .permissions import (
    PERMISSION_TAG_ATTACH, PERMISSION_TAG_CREATE, PERMISSION_TAG_DELETE,
    PERMISSION_TAG_EDIT, PERMISSION_TAG_REMOVE
)

tag_list = {'text': _('Tags'), 'view': 'tags:tag_list', 'famfam': 'tag_blue'}
tag_create = {'text': _('Create new tag'), 'view': 'tags:tag_create', 'famfam': 'tag_blue_add', 'permissions': [PERMISSION_TAG_CREATE]}

tag_attach = {'text': _('Attach tag'), 'view': 'tags:tag_attach', 'args': 'object.pk', 'famfam': 'tag_blue_add', 'permissions': [PERMISSION_TAG_ATTACH]}
tag_multiple_attach = {'text': _('Attach tag'), 'view': 'tags:tag_multiple_attach', 'famfam': 'tag_blue_add'}

multiple_documents_selection_tag_remove = {'text': _('Remove tag'), 'view': 'tags:multiple_documents_selection_tag_remove', 'famfam': 'tag_blue_delete'}
single_document_multiple_tag_remove = {'text': _('Remove tags'), 'view': 'tags:single_document_multiple_tag_remove', 'args': 'document.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}

tag_document_list = {'text': _('Tags'), 'view': 'tags:document_tags', 'args': 'object.pk', 'famfam': 'tag_blue', 'permissions': [PERMISSION_TAG_REMOVE, PERMISSION_TAG_ATTACH]}
tag_delete = {'text': _('Delete'), 'view': 'tags:tag_delete', 'args': 'object.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_edit = {'text': _('Edit'), 'view': 'tags:tag_edit', 'args': 'object.id', 'famfam': 'tag_blue_edit', 'permissions': [PERMISSION_TAG_EDIT]}
tag_tagged_item_list = {'text': _('Documents'), 'view': 'tags:tag_tagged_item_list', 'args': 'object.id', 'famfam': 'page'}
tag_multiple_delete = {'text': _('Delete'), 'view': 'tags:tag_multiple_delete', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_acl_list = {'text': _('ACLs'), 'view': 'tags:tag_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
