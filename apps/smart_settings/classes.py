from __future__ import absolute_import

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.db import transaction, DatabaseError

from .models import ClusterSetting


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


class ScopeBase(object):
    def get_value(self):
        raise NotImplemented
        
    def set_value(self):
        raise NotImplemented
        
    def register_setting(self, setting):
        self.setting = setting

    def get_full_name(self):
        return ('%s_%s' % (self.setting.namespace.name, self.setting.name)).upper()


class LocalScope(ScopeBase):
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
            self.global_name = self.get_full_name()

        return getattr(settings, self.global_name)
    

class ClusterScope(ScopeBase):
    """
    Return the value of a config value from the local settings.py file
    """
    label = _(u'Cluster')

    #def __init__(self):
    #    self.global_name = global_name
    
    def __unicode__(self):
        return unicode(self.__class__.label)
        
    def __repr__(self):
        return unicode(self.__unicode__())

    def get_value(self):
        return ClusterSetting.objects.get(name=self.get_full_name()).value

    @transaction.commit_on_success
    def register_setting(self, *args, **kwargs):
        super(ClusterScope, self).register_setting(*args, **kwargs)
        try:
            cluster_settings = ClusterSetting.objects.get_or_create(name=self.get_full_name(), defaults={'value': getattr(self.setting, 'default', None)})
        except DatabaseError:
            transaction.rollback()

# TODO: Organization - Organizaition wide preferences
# TODO: User - user preferences

# Settings
class Setting(object):
    def register_scope(self, scope):
        """
        Store this setting's instance into the scope instance and append
        the scope to this setting's scope list
        """
        scope.register_setting(self)
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
