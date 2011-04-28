from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permissions
from navigation.api import register_sidebar_template

from taggit.models import Tag

PERMISSION_TAG_CREATE = 'tag_create'
PERMISSION_TAG_ATTACH = 'tag_attach'
PERMISSION_TAG_DELETE = 'tag_delete'

register_permissions('tags', [
    {'name': PERMISSION_TAG_CREATE, 'label': _(u'Can create new tags')},
    {'name': PERMISSION_TAG_ATTACH, 'label': _(u'Can attach exising tags')},
    {'name': PERMISSION_TAG_DELETE, 'label': _(u'Can delete tags')},
])

tag_list = {'text': _('tags'), 'view': 'tag_list', 'famfam': 'tag_blue'}
tag_delete = {'text': _('delete'), 'view': 'tag_remove', 'args': ['object.id', 'document.id'], 'famfam': 'tag_blue_delete', 'permissions': {'namespace': 'tags', 'permissions': [PERMISSION_TAG_DELETE]}}

register_links(Tag, [tag_delete])

register_sidebar_template(['document_view', 'document_view_simple'], 'tags_sidebar_template.html')

tags_menu = [
    {
        'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue', 'position': 4, 'links': [
            tag_list
        ]
    },
]

#register_menu(tags_menu)
