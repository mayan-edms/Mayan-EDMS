from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (bind_links, register_top_menu,
    register_model_list_columns, register_multi_item_links, Link)
from common.utils import encapsulate
from documents.models import Document
from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL

from taggit.models import Tag
from taggit.managers import TaggableManager

from .widgets import (get_tags_inline_widget_simple, single_tag_widget)
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

register_model_list_columns(Tag, [
    {
        'name': _(u'preview'),
        'attribute': encapsulate(lambda x: single_tag_widget(x))
    },
    {
        'name': _(u'tagged items'),
        'attribute': encapsulate(lambda x: x.taggit_taggeditem_items.count())
    }
])

register_model_list_columns(Document, [
    {'name':_(u'tags'), 'attribute':
        encapsulate(lambda x: get_tags_inline_widget_simple(x))
    },
])

bind_links([Tag], [tag_tagged_item_list, tag_edit, tag_delete, tag_acl_list])
register_multi_item_links(['tag_list'], [tag_multiple_delete])
bind_links([Tag, 'tag_list', 'tag_create'], [tag_list, tag_create], menu_name='secondary_menu')
register_top_menu('tags', link={'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue'}, children_view_regex=[r'^tag_(list|create|delete|edit|tagged|acl)'])

bind_links([Document], [tag_document_list], menu_name='form_header')
bind_links(['document_tags', 'tag_remove', 'tag_multiple_remove', 'tag_attach'], [tag_attach], menu_name='sidebar')
register_multi_item_links(['document_tags'], [tag_document_remove_multiple])

class_permissions(Document, [
    PERMISSION_TAG_ATTACH,
    PERMISSION_TAG_REMOVE,
])

class_permissions(Tag, [
    PERMISSION_TAG_DELETE,
    PERMISSION_TAG_EDIT,
    PERMISSION_TAG_VIEW,
])

Document.add_to_class('tags', TaggableManager())
