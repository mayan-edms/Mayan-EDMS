from __future__ import unicode_literals

import errno
import hashlib
from importlib import import_module
import logging
import os
import sys

import yaml

from django.apps import apps
from django.conf import settings
from django.utils.functional import Promise
from django.utils.encoding import (
    force_bytes, force_text, python_2_unicode_compatible
)

from mayan.apps.common.serialization import yaml_dump, yaml_load

from .utils import read_configuration_file

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Namespace(object):
    _registry = {}

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.settings'.format(app.name))
            except ImportError as exception:
                if force_text(exception) not in ('No module named settings', 'No module named \'{}.settings\''.format(app.name)):
                    logger.error(
                        'Error importing %s settings.py file; %s', app.name,
                        exception
                    )

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.label)

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def invalidate_cache_all(cls):
        for namespace in cls.get_all():
            namespace.invalidate_cache()

    def __init__(self, name, label):
        if name in self.__class__._registry:
            raise Exception(
                'Namespace names must be unique; "%s" already exists.' % name
            )
        self.name = name
        self.label = label
        self.__class__._registry[name] = self
        self._settings = []

    def __str__(self):
        return force_text(self.label)

    def add_setting(self, **kwargs):
        return Setting(namespace=self, **kwargs)

    def invalidate_cache(self):
        for setting in self._settings:
            setting.invalidate_cache()

    @property
    def settings(self):
        return sorted(self._settings, key=lambda x: x.global_name)


@python_2_unicode_compatible
class Setting(object):
    _registry = {}
    _cache_hash = None
    _config_file_cache = None

    @staticmethod
    def deserialize_value(value):
        return yaml_load(stream=value)

    @staticmethod
    def express_promises(value):
        """
        Walk all the elements of a value and force promises to text
        """
        if isinstance(value, (list, tuple)):
            return [Setting.express_promises(item) for item in value]
        elif isinstance(value, Promise):
            return force_text(value)
        else:
            return value

    @staticmethod
    def serialize_value(value):
        result = yaml_dump(
            data=Setting.express_promises(value), allow_unicode=True,
            default_flow_style=False,
        )
        # safe_dump returns bytestrings
        # Disregard the last 3 dots that mark the end of the YAML document
        if force_text(result).endswith('...\n'):
            result = result[:-4]

        return result

    @classmethod
    def check_changed(cls):
        if not cls._cache_hash:
            cls._cache_hash = cls.get_hash()

        return cls._cache_hash != cls.get_hash()

    @classmethod
    def dump_data(cls, filter_term=None, namespace=None):
        dictionary = {}

        for setting in cls.get_all():
            if (namespace and setting.namespace.name == namespace) or not namespace:
                if (filter_term and filter_term.lower() in setting.global_name.lower()) or not filter_term:
                    dictionary[setting.global_name] = Setting.express_promises(setting.value)

        return yaml_dump(
            data=dictionary, default_flow_style=False
        )

    @classmethod
    def get(cls, global_name):
        return cls._registry[global_name]

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.global_name)

    @classmethod
    def get_config_file_content(cls):
        # Cache content of config file to speed up initial boot up
        if not cls._config_file_cache:
            cls._config_file_cache = read_configuration_file(
                path=settings.CONFIGURATION_FILEPATH
            )

        return cls._config_file_cache

    @classmethod
    def get_hash(cls):
        return force_text(
            hashlib.sha256(force_bytes(cls.dump_data())).hexdigest()
        )

    @classmethod
    def save_configuration(cls, path=settings.CONFIGURATION_FILEPATH):
        try:
            with open(path, 'w') as file_object:
                file_object.write(cls.dump_data())
        except IOError as exception:
            if exception.errno == errno.ENOENT:
                logger.warning(
                    'The path to the configuration file doesn\'t '
                    'exist. It is not possible to save the backup file.'
                )

    @classmethod
    def save_last_known_good(cls):
        # Don't write over the last good configuration if we are trying
        # to restore the last good configuration
        if 'revertsettings' not in sys.argv:
            cls.save_configuration(
                path=settings.CONFIGURATION_LAST_GOOD_FILEPATH
            )

    def __init__(self, namespace, global_name, default, help_text=None, is_path=False):
        self.global_name = global_name
        self.default = default
        self.help_text = help_text
        self.loaded = False
        self.namespace = namespace
        self.environment_variable = False
        namespace._settings.append(self)
        self.__class__._registry[global_name] = self

    def __str__(self):
        return force_text(self.global_name)

    def cache_value(self):
        environment_value = os.environ.get('MAYAN_{}'.format(self.global_name))
        if environment_value:
            self.environment_variable = True
            try:
                self.raw_value = yaml_load(stream=environment_value)
            except yaml.YAMLError as exception:
                raise type(exception)(
                    'Error interpreting environment variable: {} with '
                    'value: {}; {}'.format(
                        self.global_name, environment_value, exception
                    )
                )
        else:
            self.raw_value = self.get_config_file_content().get(
                self.global_name, getattr(
                    settings, self.global_name, self.default
                )
            )

        self.yaml = Setting.serialize_value(self.raw_value)
        self.loaded = True

    def invalidate_cache(self):
        self.loaded = False

    @property
    def serialized_value(self):
        """
        YAML serialize value of the setting.
        Used for UI display.
        """
        if not self.loaded:
            self.cache_value()

        return self.yaml

    @property
    def value(self):
        if not self.loaded:
            self.cache_value()

        return self.raw_value

    @value.setter
    def value(self, value):
        # value is in YAML format
        self.yaml = value
        self.raw_value = Setting.deserialize_value(value)
