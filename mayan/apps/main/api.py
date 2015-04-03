from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy

diagnostics = {}
tools = {}


def register_maintenance_links(links, title=None, namespace=None):
    namespace_dict = tools.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    for link in links:
        namespace_dict['links'].append(link)
    tools[namespace] = namespace_dict
