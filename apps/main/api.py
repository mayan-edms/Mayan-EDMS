from django.core.urlresolvers import reverse

diagnostics = {}


def register_diagnostic(namespace, title, link):
    namespace_dict = diagnostics.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    link['url'] = link.get('url', reverse(link['view']))
    namespace_dict['links'].append(link)
    diagnostics[namespace] = namespace_dict
