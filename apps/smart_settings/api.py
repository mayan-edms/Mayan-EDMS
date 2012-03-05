from __future__ import absolute_import

from django.conf import settings as django_settings
from django.utils.importlib import import_module

from django.utils.translation import ugettext_lazy as _
from navigation.api import register_links

settings = {}
settings_list = []
namespace_list = []


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


class SettingNamespace(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label
        link = {'text': 'LINK', 'view': 'settings_list', 'args': name, 'famfam': 'pencil_add'}#, 'permissions': [PERMISSION_SIGNATURE_UPLOAD], 'conditional_disable': has_embedded_signature}
        register_links(['about_view'], [link], menu_name='sidebar')

        print 'namespace', self
        
        namespace_list.append(self)

    def __unicode__(self):
        return unicode(self.label)
        
    def settings(self):
        return [setting for setting in settings_list if setting.namespace == self]
        

class Setting(object):
    def __init__(self, namespace, module, name, global_name, default, description=None, hidden=False, exists=False):
        self.namespace = namespace
        self.name = name
        self.global_name = global_name
        self.default = default
        self.description = description
        self.hidden = hidden
        self.exists = exists
       
        # Get the global value
        value = getattr(django_settings, global_name, default)

        # Create the local entity
        try:
            setattr(module, name, value)
            self.module = module
        except AttributeError:
            self.module = import_module(module)
            setattr(self.module, name, value)

        settings_list.append(self)


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
