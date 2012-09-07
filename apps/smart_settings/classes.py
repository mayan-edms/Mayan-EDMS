from __future__ import absolute_import

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _


# Namespace
class SettingsNamespace(object):
    _registry = {}
    _settings = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()
    
    @classmethod
    def get(cls, name):
        return cls._registry.get(name)

    def __init__(self, name, label, module):
        self.name = name
        self.label = label
        self.module = module

        self.__class__._registry[self.name] = self

    def __unicode__(self):
        return unicode(self.label)
        
    def register(self, setting):
        self.__class__._settings.setdefault(self.name, {})
        self.__class__._settings[self.name][setting.name] = setting

    def add_setting(self, *args, **kwargs):
        return Setting(namespace=self, *args, **kwargs)

    def get_settings(self):
        return self.__class__._settings[self.name].values()


# Scopes
class SettingScope(object):
    def get_value(self):
        raise NotImplemented


class LocalScope(SettingScope):
    """
    Return the value of a config value from the local settings.py file
    """
    label = _(u'Local')

    def __init__(self, global_name=None):
        self.global_name = global_name
    
    def __unicode__(self):
        return u'%s: %s' % (self.__class__.label, self.global_name)
        
    def __repr__(self):
        return unicode(self.__unicode__())

    def get_value(self):
        if not self.global_name:
            self.global_name = '%s_%s' % (self.setting.namespace.name.upper(), self.setting.name)
            
        return getattr(settings, self.global_name)


# TODO: Cluster - Cluster wide setting
# TODO: Organization - Organizaition wide preferences
# TODO: User - user preferences

# Settings
class Setting(object):
    def register_scope(self, scope):
        """
        Store this setting's instance into the scope instance and append
        the scope to this setting's scope list
        """
        scope.setting = self
        self.scopes.append(scope)

    def __init__(self, namespace, name, default, description=None, hidden=False, exists=False, scopes=None):
        self.namespace = namespace
        self.name = name
        self.default = default
        self.description = description
        self.hidden = hidden
        self.exists = exists
        self.scopes = []
        
        if scopes:
            for scope in scopes:
                self.register_scope(scope)
        #else:
        #    self.scopes = []  #Local('GLOBAL_%s' % self.app.name)]

        # Get the global value
        #value = getattr(django_settings, global_name, default)
        # Create the local entity
        #try:
        #    #self.module = namespace.module
        #    setattr('%s.settings' % self.app.name, self.name, value)
        #except AttributeError:
        #module = import_module(self.app.name)
        #print module
        #setattr(module, 'conf.settings.%s'  % self.name, value)
        #setattr(module, 'conf.%s'  % self.name, value)
        #setattr(module, self.name, value)

        # Create the local entity
        try:
            self.module = namespace.module
            setattr(self.module, name, self.get_value())
        except AttributeError:
            self.module = import_module(namespace.module)
            setattr(self.module, name, self.get_value())

        # Register with the namespace
        self.namespace.register(self)

    def get_value(self):
        value = self.default
        for scopes in self.scopes:
            try:
                value = scopes.get_value()
            except Exception:
                pass

        return value

    def get_scopes_display(self):
        return u', '.join([unicode(scope) for scope in self.scopes])
