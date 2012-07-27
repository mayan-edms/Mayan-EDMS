from common.utils import reverse_lazy

tools = {}


def register_maintenance_links(links, title=None, namespace=None):
    namespace_dict = tools.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    for link in links:
        link.url = getattr(link, 'url', reverse_lazy(link.view))
        namespace_dict['links'].append(link)
    tools[namespace] = namespace_dict
