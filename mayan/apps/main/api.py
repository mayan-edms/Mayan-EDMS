from django.core.urlresolvers import reverse
from django.utils.functional import lazy

diagnostics = {}
tools = {}
# TODO: Use Django's included reverse_lazy
reverse_lazy = lazy(reverse, str)


def register_maintenance_links(links, title=None, namespace=None):
    namespace_dict = tools.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    for link in links:
        link['url'] = link.get('url', reverse_lazy(link['view']))
        namespace_dict['links'].append(link)
    tools[namespace] = namespace_dict
