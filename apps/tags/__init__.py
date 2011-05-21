from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permissions
from navigation.api import register_sidebar_template

from taggit.models import Tag

PERMISSION_TAG_CREATE = 'tag_create'
PERMISSION_TAG_ATTACH = 'tag_attach'
PERMISSION_TAG_REMOVE = 'tag_remove'
PERMISSION_TAG_DELETE = 'tag_delete'
PERMISSION_TAG_EDIT = 'tag_edit'

register_permissions('tags', [
    {'name': PERMISSION_TAG_CREATE, 'label': _(u'Create new tags')},
    {'name': PERMISSION_TAG_ATTACH, 'label': _(u'Attach exising tags')},
    {'name': PERMISSION_TAG_REMOVE, 'label': _(u'Remove tags from documents')},
    {'name': PERMISSION_TAG_DELETE, 'label': _(u'Delete global tags')},
    {'name': PERMISSION_TAG_EDIT, 'label': _(u'Edit global tags')},
])

tag_list = {'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue'}
tag_document_remove = {'text': _(u'remove'), 'view': 'tag_remove', 'args': ['object.id', 'document.id'], 'famfam': 'tag_blue_delete', 'permissions': {'namespace': 'tags', 'permissions': [PERMISSION_TAG_REMOVE]}}
tag_delete = {'text': _(u'delete'), 'view': 'tag_delete', 'args': 'object.id', 'famfam': 'tag_blue_delete', 'permissions': {'namespace': 'tags', 'permissions': [PERMISSION_TAG_DELETE]}}
tag_edit = {'text': _(u'edit'), 'view': 'tag_edit', 'args': 'object.id', 'famfam': 'tag_blue_edit', 'permissions': {'namespace': 'tags', 'permissions': [PERMISSION_TAG_EDIT]}}
tag_tagged_item_list = {'text': _(u'tagged documents'), 'view': 'tag_tagged_item_list', 'args': 'object.id', 'famfam': 'tag_blue'}
tag_multiple_delete = {'text': _(u'delete'), 'view': 'tag_multiple_delete', 'famfam': 'tag_blue_delete', 'permissions': {'namespace': 'tags', 'permissions': [PERMISSION_TAG_DELETE]}}

register_model_list_columns(Tag, [
    {
        'name': _(u'color'),
        'attribute': lambda x: u'<div style="width: 20px; height: 20px; border: 1px solid black; background: %s;"></div>' %
            x.tagproperties_set.get().get_color_code(),
    },
    {
        'name': _(u'color name'),
        'attribute': lambda x: x.tagproperties_set.get().get_color_display(),
    }
])

register_links(Tag, [tag_tagged_item_list, tag_edit])

register_multi_item_links(['tag_list'], [tag_multiple_delete])

register_sidebar_template(['document_view_advanced', 'document_view_simple'], 'tags_sidebar_template.html')

tags_menu = [
    {
        'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue', 'position': 4, 'links': [
            tag_list
        ]
    },
]
register_menu(tags_menu)
