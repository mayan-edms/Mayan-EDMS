from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL

from .permissions import (PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_VIEW)

tag_list = {'text': _(u'tag list'), 'view': 'tag_list', 'famfam': 'tag_blue'}
tag_create = {'text': _(u'create new tag'), 'view': 'tag_create', 'famfam': 'tag_blue_add', 'permissions': [PERMISSION_TAG_CREATE]}

tag_attach = {'text': _(u'attach tag'), 'view': 'tag_attach', 'args': 'object.pk', 'famfam': 'tag_blue_add', 'permissions': [PERMISSION_TAG_ATTACH]}
tag_multiple_attach = {'text': _(u'attach tag'), 'view': 'tag_multiple_attach', 'famfam': 'tag_blue_add'}

#tag_remove = {'text': _(u'remove tag'), 'view': 'tag_remove', 'args': 'object.pk', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}
multiple_documents_selection_tag_remove = {'text': _(u'remove tag'), 'view': 'multiple_documents_selection_tag_remove', 'famfam': 'tag_blue_delete'}
single_document_multiple_tag_remove = {'text': _(u'remove tags'), 'view': 'single_document_multiple_tag_remove', 'args': 'document.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}

tag_document_list = {'text': _(u'tags'), 'view': 'document_tags', 'args': 'object.pk', 'famfam': 'tag_blue', 'permissions': [PERMISSION_TAG_REMOVE, PERMISSION_TAG_ATTACH], 'children_view_regex': ['tag']}
tag_delete = {'text': _(u'delete'), 'view': 'tag_delete', 'args': 'object.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_edit = {'text': _(u'edit'), 'view': 'tag_edit', 'args': 'object.id', 'famfam': 'tag_blue_edit', 'permissions': [PERMISSION_TAG_EDIT]}
tag_tagged_item_list = {'text': _(u'tagged documents'), 'view': 'tag_tagged_item_list', 'args': 'object.id', 'famfam': 'page'}
tag_multiple_delete = {'text': _(u'delete'), 'view': 'tag_multiple_delete', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_acl_list = {'text': _(u'ACLs'), 'view': 'tag_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
