from __future__ import unicode_literals

from importlib import import_module
import logging

import yaml

from django.apps import apps
from django.conf import settings
from django.utils.functional import Promise
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)


class Namespace(object):
    _registry = {}

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.settings'.format(app.name))
            except ImportError:
                logger.debug('App %s has no settings.py file', app.name)
            else:
                logger.debug(
                    'Imported settings.py file for app %s', app.name
                )

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def invalidate_cache_all(cls):
        for namespace in cls.get_all():
            namespace.invalidate_cache()

    def __unicode__(self):
        return unicode(self.label)

    def __init__(self, name, label):
        if name in self.__class__._registry:
            raise Exception(
                'Namespace names must be unique; "%s" already exists.' % name
            )
        self.name = name
        self.label = label
        self.__class__._registry[name] = self
        self.settings = []

    def add_setting(self, **kwargs):
        return Setting(namespace=self, **kwargs)

    def invalidate_cache(self):
        for setting in self.settings:
            setting.invalidate_cache()


class Setting(object):
    @staticmethod
    def deserialize_value(value):
        return yaml.safe_load(value)

    @staticmethod
    def serialize_value(value):
        if isinstance(value, Promise):
            value = force_text(value)

        return yaml.safe_dump(value, allow_unicode=True)

    def __init__(self, namespace, global_name, default, help_text=None, is_path=False):
        self.global_name = global_name
        self.default = default
        self.help_text = help_text
        self.loaded = False
        namespace.settings.append(self)

    def __unicode__(self):
        return unicode(self.global_name)

    def invalidate_cache(self):
        self.loaded = False

    @property
    def serialized_value(self):
        return self.yaml

    @property
    def value(self):
        if not self.loaded:
            self.raw_value = getattr(settings, self.global_name, self.default)
            self.yaml = Setting.serialize_value(self.raw_value)
            self.loaded = True

        return self.raw_value

    @value.setter
    def value(self, value):
        # value is in YAML format
        self.yaml = value
        self.raw_value = Setting.deserialize_value(value)
