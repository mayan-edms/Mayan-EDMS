diagnostics = {}


def register_diagnostic(namespace, title, link):
    namespace_dict = diagnostics.get(namespace, {'title': None, 'links': []})
    namespace_dict['title'] = title
    namespace_dict['links'].append(link)
    diagnostics[namespace] = namespace_dict
