from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from permissions.api import register_permissions
from navigation.api import register_sidebar_template

from taggit.models import Tag

tag_delete = {'text': _('delete'), 'view': 'tag_remove', 'args': ['object.id', 'document.id'], 'famfam': 'tag_blue_delete'}#, 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DELETE]}}


register_links(Tag, [tag_delete])

register_sidebar_template(['document_view', 'document_view_simple'], 'tags_sidebar_template.html')
