from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.utils import encapsulate
from documents.models import Document
from navigation.api import (
    register_links, register_model_list_columns, register_top_menu
)
from navigation.links import link_spacer
from rest_api.classes import APIEndPoint

from .links import (
    multiple_documents_selection_tag_remove,
    single_document_multiple_tag_remove, tag_acl_list, tag_attach, tag_create,
    tag_delete, tag_document_list, tag_edit, tag_list, tag_multiple_attach,
    tag_multiple_delete, tag_tagged_item_list
)
from .models import Tag
from .permissions import (
    PERMISSION_TAG_ATTACH, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_VIEW
)
from .widgets import get_tags_inline_widget_simple, single_tag_widget

class_permissions(Document, [
    PERMISSION_TAG_ATTACH, PERMISSION_TAG_REMOVE,
])
class_permissions(Tag, [
    PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT, PERMISSION_TAG_VIEW,
])

APIEndPoint('tags')

register_model_list_columns(Tag, [
    {
        'name': _('Preview'),
        'attribute': encapsulate(lambda x: single_tag_widget(x))
    },
    {
        'name': _('Tagged items'),
        'attribute': encapsulate(lambda x: x.documents.count())
    }
])

register_model_list_columns(Document, [
    {
        'name': _('Tags'), 'attribute':
        encapsulate(lambda x: get_tags_inline_widget_simple(x))
    },
])

register_top_menu('tags', link={'text': _('Tags'), 'view': 'tags:tag_list', 'famfam': 'tag_blue'})

register_links(Tag, [tag_tagged_item_list, tag_edit, tag_acl_list, tag_delete])
register_links([Tag], [tag_multiple_delete], menu_name='multi_item_links')
register_links([Tag, 'tags:tag_list', 'tags:tag_create'], [tag_list, tag_create], menu_name='secondary_menu')

register_links(Document, [tag_document_list], menu_name='form_header')
register_links(['tags:document_tags', 'tags:tag_remove', 'tags:tag_multiple_remove', 'tags:tag_attach'], [tag_attach], menu_name='sidebar')
register_links(['tags:document_tags'], [single_document_multiple_tag_remove], menu_name='multi_item_links')
register_links([Document], [tag_multiple_attach, multiple_documents_selection_tag_remove, link_spacer], menu_name='multi_item_links')
