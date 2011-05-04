from django.utils.translation import ugettext_lazy as _


from permissions.api import register_permissions
from main.api import register_tool


FILESYSTEM_SERVING_RECREATE_LINKS = 'recreate_links'

register_permissions('filesystem_serving', [
    {'name': FILESYSTEM_SERVING_RECREATE_LINKS, 'label':_(u'Recreate filesystem links.')},
])

filesystem_serving_recreate_all_links = {'text': _('recreate index links'), 'view': 'recreate_all_links', 'famfam': 'page_link', 'permissions': {'namespace': 'filesystem_serving', 'permissions': [FILESYSTEM_SERVING_RECREATE_LINKS]}, 'description': _(u'Deletes and creates from scratch all the file system indexing links.')}

register_tool(filesystem_serving_recreate_all_links, namespace='filesystem_serving', title=_(u'Filesystem'))
