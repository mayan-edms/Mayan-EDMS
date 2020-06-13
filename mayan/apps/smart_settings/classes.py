import errno
import hashlib
import logging
import os
import re
import sys

import yaml

from django.conf import settings
from django.utils.functional import Promise
from django.utils.encoding import (
    force_bytes, force_text
)
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.serialization import yaml_dump, yaml_load

from .literals import (
    NAMESPACE_VERSION_INITIAL, SMART_SETTINGS_NAMESPACES_NAME
)

logger = logging.getLogger(name=__name__)


def read_configuration_file(filepath):
    try:
        with open(file=filepath) as file_object:
            file_object.seek(0, os.SEEK_END)
            if file_object.tell():
                file_object.seek(0)
                try:
                    return yaml_load(stream=file_object)
                except yaml.YAMLError as exception:
                    exit(
                        'Error loading configuration file: {}; {}'.format(
                            filepath, exception
                        )
                    )
    except IOError as exception:
        if exception.errno == errno.ENOENT:
            # No config file, return empty dictionary
            return {}
        else:
            raise


class SettingNamespace(AppsModuleLoaderMixin):
    _loader_module_name = 'settings'
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(cls._registry.values(), key=lambda x: x.label)

    @classmethod
    def get_namespace_config(cls, name):
        return cls.get_namespaces_config().get(name, {})

    @classmethod
    def get_namespaces_config(cls):
        return Setting.get_config_file_content().get(SMART_SETTINGS_NAMESPACES_NAME, {})

    @classmethod
    def invalidate_cache_all(cls):
        for namespace in cls.get_all():
            namespace.invalidate_cache()

    def __init__(
        self, name, label, migration_class=None,
        version=NAMESPACE_VERSION_INITIAL
    ):
        if name in self.__class__._registry:
            raise Exception(
                'Namespace names must be unique; "%s" already exists.' % name
            )
        self.migration_class = migration_class
        self.name = name
        self.label = label
        self.version = version
        self.__class__._registry[name] = self
        self._settings = []

    def __str__(self):
        return force_text(self.label)

    def add_setting(self, **kwargs):
        return Setting(namespace=self, **kwargs)

    def get_config_version(self):
        return SettingNamespace.get_namespace_config(name=self.name).get(
            'version', NAMESPACE_VERSION_INITIAL
        )

    def invalidate_cache(self):
        for setting in self._settings:
            setting.invalidate_cache()

    def migrate(self, setting):
        if self.migration_class:
            self.migration_class(namespace=self).migrate(setting=setting)

    @property
    def settings(self):
        return sorted(self._settings, key=lambda x: x.global_name)


class SettingNamespaceMigration:
    @staticmethod
    def get_method_name(setting):
        return setting.global_name.lower()

    def __init__(self, namespace):
        self.namespace = namespace

    def get_method_name_full(self, setting, version):
        return '{}_{}'.format(
            self.get_method_name(setting=setting),
            version
        )

    def migrate(self, setting):
        if self.namespace.get_config_version() != self.namespace.version:
            setting_method_name = SettingNamespaceMigration.get_method_name(
                setting=setting
            )

            # Get methods for this setting
            pattern = r'{}_\d{{4}}'.format(setting_method_name)
            setting_methods = re.findall(
                pattern=pattern, string='\n'.join(dir(self))
            )

            # Get order of execution of setting methods
            versions = [
                method.replace(
                    '{}_'.format(setting_method_name), ''
                ) for method in setting_methods
            ]
            try:
                start = versions.index(self.namespace.get_config_version())
            except ValueError:
                start = 0

            try:
                end = versions.index(self.namespace.version)
            except ValueError:
                end = None

            value = setting.raw_value
            for version in versions[start:end]:
                method = getattr(
                    self, self.get_method_name_full(
                        setting=setting, version=version
                    ), None
                )
                if method:
                    value = method(value=value)

            setting.raw_value = value


class Setting:
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

        if not namespace:
            namespace_dictionary = {}
            for _namespace in SettingNamespace.get_all():
                namespace_dictionary[_namespace.name] = {
                    'version': _namespace.version
                }

            dictionary[SMART_SETTINGS_NAMESPACES_NAME] = namespace_dictionary

        for setting in cls.get_all():
            # If a namespace is specified, filter the list by that namespace
            # otherwise return always True to include all (or not None == True)
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
                filepath=settings.CONFIGURATION_FILEPATH
            ) or {}
        return cls._config_file_cache

    @classmethod
    def get_hash(cls):
        return force_text(
            hashlib.sha256(force_bytes(cls.dump_data())).hexdigest()
        )

    @classmethod
    def save_configuration(cls, path=None):
        if not path:
            path = settings.CONFIGURATION_FILEPATH

        try:
            with open(file=path, mode='w') as file_object:
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

    def __init__(
        self, namespace, global_name, default, help_text=None, is_path=False,
        post_edit_function=None
    ):
        self.global_name = global_name
        self.default = default
        self.help_text = help_text
        self.loaded = False
        self.namespace = namespace
        self.environment_variable = False
        self.post_edit_function = post_edit_function
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
            try:
                # Try the config file
                self.raw_value = self.get_config_file_content()[self.global_name]
            except KeyError:
                try:
                    # Try the Django settings variable
                    self.raw_value = getattr(
                        settings, self.global_name
                    )
                except AttributeError:
                    # Finally set to the default value
                    self.raw_value = self.default
            else:
                # Found in the config file, try to migrate the value
                self.migrate()

        self.yaml = Setting.serialize_value(self.raw_value)
        self.loaded = True

    def invalidate_cache(self):
        self.loaded = False

    def is_overridden(self):
        return self.environment_variable

    is_overridden.short_description = _('Overridden')
    is_overridden.help_text = _(
        'Is this settings being overridden by an environment variable?'
    )

    def migrate(self):
        self.namespace.migrate(setting=self)

    @property
    def serialized_value(self):
        """
        YAML serialize value of the setting.
        Used for UI display.
        """
        if not self.loaded:
            self.cache_value()

        return self.yaml

    def set(self, value):
        self.value = Setting.serialize_value(value=value)

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
        if self.post_edit_function:
            self.post_edit_function(setting=self)
