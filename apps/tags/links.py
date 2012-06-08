from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link
from acls.permissions import ACLS_VIEW_ACL

from .permissions import (PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_VIEW)

tag_list = Link(text=_(u'tag list'), view='tag_list', sprite='tag_blue')
tag_create = Link(text=_(u'create new tag'), view='tag_create', sprite='tag_blue_add', permissions=[PERMISSION_TAG_CREATE])
tag_attach = Link(text=_(u'attach tag'), view='tag_attach', args='object.pk', sprite='tag_blue_add', permissions=[PERMISSION_TAG_ATTACH])
tag_document_remove = Link(text=_(u'remove'), view='tag_remove', args=['object.pk', 'document.pk'], sprite='tag_blue_delete', permissions=[PERMISSION_TAG_REMOVE])
tag_document_remove_multiple = Link(text=_(u'remove'), view='tag_multiple_remove', args='document.pk', sprite='tag_blue_delete', permissions=[PERMISSION_TAG_REMOVE])
tag_document_list = Link(text=_(u'tags'), view='document_tags', args='object.pk', sprite='tag_blue', permissions=[PERMISSION_TAG_REMOVE, PERMISSION_TAG_ATTACH], children_view_regex=['tag'])
tag_delete = Link(text=_(u'delete'), view='tag_delete', args='object.pk', sprite='tag_blue_delete', permissions=[PERMISSION_TAG_DELETE])
tag_edit = Link(text=_(u'edit'), view='tag_edit', args='object.pk', sprite='tag_blue_edit', permissions=[PERMISSION_TAG_EDIT])
tag_tagged_item_list = Link(text=_(u'tagged documents'), view='tag_tagged_item_list', args='object.pk', sprite='page')
tag_multiple_delete = Link(text=_(u'delete'), view='tag_multiple_delete', sprite='tag_blue_delete', permissions=[PERMISSION_TAG_DELETE])
tag_acl_list = Link(text=_(u'ACLs'), view='tag_acl_list', args='object.pk', sprite='lock', permissions=[ACLS_VIEW_ACL])
