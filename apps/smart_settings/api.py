from __future__ import absolute_import

from django.conf import settings as django_settings
from django.utils.importlib import import_module

from django.utils.translation import ugettext_lazy as _

settings = {}
settings_list = []
namespace_list = []


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


class SettingNamespace(object):
    def __init__(self, name, label, module):
        self.name = name
        self.label = label
        self.module = module
        namespace_list.append(self)

    def __unicode__(self):
        return unicode(self.label)
        
    def settings(self):
        return [setting for setting in settings_list if setting.namespace == self]
        

class Setting(object):
    def __init__(self, namespace, name, global_name, default, description=u'', hidden=False, exists=False):
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
            self.module = namespace.module
            setattr(self.module, name, value)
        except AttributeError:
            self.module = import_module(namespace.module)
            setattr(self.module, name, value)

        settings_list.append(self)
