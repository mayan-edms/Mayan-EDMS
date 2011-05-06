from django.core.urlresolvers import reverse
from django.utils.functional import lazy

diagnostics = {}
tools = {}
reverse_lazy = lazy(reverse, str)


def register_diagnostic(namespace, title, link):
    namespace_dict = diagnostics.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    link['url'] = link.get('url', reverse_lazy(link['view']))
    namespace_dict['links'].append(link)
    diagnostics[namespace] = namespace_dict


def register_tool(link, title=None, namespace=None):
    namespace_dict = tools.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    link['url'] = link.get('url', reverse_lazy(link['view']))
    namespace_dict['links'].append(link)
    tools[namespace] = namespace_dict
