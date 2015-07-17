from __future__ import unicode_literals

import yaml

from django.conf import settings


class Namespace(object):
    _registry = {}

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __unicode__(self):
        return unicode(self.label)

    def __init__(self, name, label):
        if name in self.__class__._registry:
            raise Exception('Namespace names must be unique; "%s" already exists.' % name)
        self.name = name
        self.label = label
        self.__class__._registry[name] = self
        self.settings = []

    def add_setting(self, **kwargs):
        return Setting(namespace=self, **kwargs)


class Setting(object):
    def __init__(self, namespace, global_name, default, help_text=None, is_path=False):
        self.global_name = global_name
        self.default = default
        self.help_text = help_text
        self.is_path = is_path
        self.yaml = None
        namespace.settings.append(self)

    def __unicode__(self):
        return unicode(self.global_name)

    @property
    def serialized_value(self):
        if not self.yaml:
            self.yaml = yaml.safe_dump(getattr(settings, self.global_name, self.default), allow_unicode=True)

        return self.yaml

    @serialized_value.setter
    def serialized_value(self, value):
        self.yaml = value

    @property
    def value(self):
        return yaml.safe_load(self.serialized_value)

    @value.setter
    def value(self, value):
        self.serialized_value = value
