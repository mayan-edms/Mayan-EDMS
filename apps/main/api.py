from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.conf import settings as django_settings
from django.utils.importlib import import_module

diagnostics = {}
tools = {}
reverse_lazy = lazy(reverse, str)
settings = {}


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


def register_setting(namespace, module, name, global_name, default, exists=False, description=u'', hidden=False):
    # Create namespace if it doesn't exists
    settings.setdefault(namespace, [])
    
    # If passed a string and not a module, import it
    if isinstance(module, basestring):
        module = import_module(module)
    
    setting = {
        'module': module,
        'name': name,
        'global_name': global_name,
        'exists': exists,
        'description': description,
        'default': default,
        'hidden': hidden,
    }
    
    # Avoid multiple appends
    if setting not in settings[namespace]:
        settings[namespace].append(setting)
        
    # Get the global value
    value = getattr(django_settings, global_name, default)
    
    # Create the local entity
    setattr(module, name, value)
    return value


def register_settings(namespace, module, settings):
    for setting in settings:
        register_setting(
            namespace,
            module,
            setting['name'],
            setting['global_name'],
            setting['default'],
            setting.get('exists', False),
            setting.get('description', u''),
            setting.get('hidden', False),
        )
