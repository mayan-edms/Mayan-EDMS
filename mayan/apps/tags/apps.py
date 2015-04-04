from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from common.menus import (
    menu_facet, menu_secondary, menu_object, menu_main, menu_multi_item,
    menu_sidebar
)
from common.utils import encapsulate
from documents.models import Document
from navigation import CombinedSource
from navigation.api import register_model_list_columns
from rest_api.classes import APIEndPoint

from .links import (
    link_multiple_documents_selection_tag_remove,
    link_single_document_multiple_tag_remove, link_tag_acl_list,
    link_tag_attach, link_tag_create, link_tag_delete, link_tag_document_list,
    link_tag_edit, link_tag_list, link_tag_multiple_attach,
    link_tag_multiple_delete, link_tag_tagged_item_list
)
from .models import Tag
from .permissions import (
    PERMISSION_TAG_ATTACH, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_VIEW
)
from .widgets import get_tags_inline_widget_simple, single_tag_widget


class TagsApp(apps.AppConfig):
    name = 'tags'
    verbose_name = _('Tags')

    def ready(self):
        APIEndPoint('tags')

        class_permissions(Document, [
            PERMISSION_TAG_ATTACH, PERMISSION_TAG_REMOVE,
        ])
        class_permissions(Tag, [
            PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT, PERMISSION_TAG_VIEW,
        ])

        menu_facet.bind_links(links=[link_tag_document_list], sources=[Document])
        menu_main.bind_links(links=[link_tag_list])
        menu_multi_item.bind_links(links=[link_tag_multiple_delete], sources=[Tag])
        menu_multi_item.bind_links(links=[link_single_document_multiple_tag_remove], sources=[CombinedSource(obj=Tag, view='tags:document_tags')])
        menu_object.bind_links(links=[link_tag_tagged_item_list, link_tag_edit, link_tag_acl_list, link_tag_delete], sources=[Tag])
        menu_secondary.bind_links(links=[link_tag_list, link_tag_create], sources=[Tag, 'tags:tag_list', 'tags:tag_create'])
        menu_sidebar.bind_links(links=[link_tag_attach], sources=['tags:document_tags', 'tags:tag_remove', 'tags:tag_multiple_remove', 'tags:tag_attach'])

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
