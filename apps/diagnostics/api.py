from common.utils import reverse_lazy

diagnostics = {}


def register_diagnostic(namespace, title, link):
    namespace_dict = diagnostics.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    link.url = getattr(link, 'url', reverse_lazy(link.view))
    namespace_dict['links'].append(link)
    diagnostics[namespace] = namespace_dict
