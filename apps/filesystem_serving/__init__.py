from django.utils.translation import ugettext_lazy as _


from permissions.api import register_permissions


FILESYSTEM_SERVING_RECREATE_LINKS = 'recreate_links'

register_permissions('filesystem_serving', [
    {'name':FILESYSTEM_SERVING_RECREATE_LINKS, 'label':_(u'Recreate filesystem links.')},
])


filesystem_serving_recreate_all_links = {'text':_('recreate index links'), 'view':'recreate_all_links', 'famfam':'page_link', 'permissions':{'namespace':'filesystem_serving', 'permissions':[FILESYSTEM_SERVING_RECREATE_LINKS]}}
