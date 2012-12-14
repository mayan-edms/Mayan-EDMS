from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document
from navigation.api import (bind_links, register_top_menu,
    register_model_list_columns, register_multi_item_links)
from acls.api import class_permissions

from taggit.models import Tag
from taggit.managers import TaggableManager

from .links import (tag_list, tag_create, tag_attach, tag_document_remove_multiple,
    tag_menu_link, tag_document_list, tag_delete, tag_edit,
    tag_tagged_item_list, tag_multiple_delete, tag_acl_list,
    tag_multiple_attach, single_document_multiple_tag_remove,
    multiple_documents_selection_tag_remove)
from .permissions import (PERMISSION_TAG_ATTACH, PERMISSION_TAG_REMOVE,
    PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT, PERMISSION_TAG_VIEW)
from .widgets import (get_tags_inline_widget_simple, single_tag_widget)

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
register_top_menu('tags', link=tag_menu_link)

bind_links([Document], [tag_document_list], menu_name='form_header')
bind_links(['document_tags', 'tag_remove', 'tag_multiple_remove', 'tag_attach'], [tag_attach], menu_name='sidebar')
register_multi_item_links(['document_tags'], [tag_document_remove_multiple])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [tag_multiple_attach, multiple_documents_selection_tag_remove])

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
