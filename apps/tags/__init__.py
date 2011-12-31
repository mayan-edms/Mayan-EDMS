from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from common.utils import encapsulate
from documents.models import Document

from taggit.models import Tag
from taggit.managers import TaggableManager

from tags.widgets import tag_color_block

PERMISSION_TAG_CREATE = {'namespace': 'tags', 'name': 'tag_create', 'label': _(u'Create new tags')}
PERMISSION_TAG_ATTACH = {'namespace': 'tags', 'name': 'tag_attach', 'label': _(u'Attach exising tags')}
PERMISSION_TAG_REMOVE = {'namespace': 'tags', 'name': 'tag_remove', 'label': _(u'Remove tags from documents')}
PERMISSION_TAG_DELETE = {'namespace': 'tags', 'name': 'tag_delete', 'label': _(u'Delete global tags')}
PERMISSION_TAG_EDIT = {'namespace': 'tags', 'name': 'tag_edit', 'label': _(u'Edit global tags')}
PERMISSION_TAG_VIEW = {'namespace': 'tags', 'name': 'tag_view', 'label': _(u'View a document\'s tags')}

set_namespace_title('tags', _(u'Tags'))
register_permission(PERMISSION_TAG_CREATE)
register_permission(PERMISSION_TAG_ATTACH)
register_permission(PERMISSION_TAG_REMOVE)
register_permission(PERMISSION_TAG_DELETE)
register_permission(PERMISSION_TAG_EDIT)
register_permission(PERMISSION_TAG_VIEW)

tag_list = {'text': _(u'tag list'), 'view': 'tag_list', 'famfam': 'tag_blue'}
tag_create = {'text': _(u'create new tag'), 'view': 'tag_create', 'famfam': 'tag_blue_add'}
tag_add_attach = {'text': _(u'attach tag'), 'view': 'tag_add_attach', 'args': 'object.pk', 'famfam': 'tag_blue_add', 'permission': [PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH]}
tag_document_remove = {'text': _(u'remove'), 'view': 'tag_remove', 'args': ['object.id', 'document.id'], 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}
tag_document_remove_multiple = {'text': _(u'remove'), 'view': 'tag_multiple_remove', 'args': 'document.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_REMOVE]}
tag_document_list = {'text': _(u'tags'), 'view': 'document_tags', 'args': 'object.pk', 'famfam': 'tag_blue', 'permissions': [PERMISSION_TAG_REMOVE], 'children_view_regex': ['tag']}
tag_delete = {'text': _(u'delete'), 'view': 'tag_delete', 'args': 'object.id', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}
tag_edit = {'text': _(u'edit'), 'view': 'tag_edit', 'args': 'object.id', 'famfam': 'tag_blue_edit', 'permissions': [PERMISSION_TAG_EDIT]}
tag_tagged_item_list = {'text': _(u'tagged documents'), 'view': 'tag_tagged_item_list', 'args': 'object.id', 'famfam': 'page'}
tag_multiple_delete = {'text': _(u'delete'), 'view': 'tag_multiple_delete', 'famfam': 'tag_blue_delete', 'permissions': [PERMISSION_TAG_DELETE]}

register_model_list_columns(Tag, [
    {
        'name': _(u'color'),
        'attribute': encapsulate(lambda x: tag_color_block(x))
    },
    {
        'name': _(u'color name'),
        'attribute': encapsulate(lambda x: x.tagproperties_set.get().get_color_display()),
    }
])

register_links(Tag, [tag_tagged_item_list, tag_edit, tag_delete])

register_multi_item_links(['tag_list'], [tag_multiple_delete])

register_links(['tag_list', 'tag_delete', 'tag_edit', 'tag_tagged_item_list', 'tag_multiple_delete', 'tag_create'], [tag_list, tag_create], menu_name='secondary_menu')

#register_sidebar_template(['document_tags'], 'tags_sidebar_template.html')

register_top_menu('tags', link={'text': _(u'tags'), 'view': 'tag_list', 'famfam': 'tag_blue'}, children_path_regex=[r'^tags/[^d]'])

register_links(Document, [tag_document_list], menu_name='form_header')
register_links(['document_tags', 'tag_add_attach', 'tag_remove', 'tag_multiple_remove'], [tag_add_attach], menu_name='sidebar')

register_multi_item_links(['document_tags'], [tag_document_remove_multiple])

Document.add_to_class('tags', TaggableManager())
