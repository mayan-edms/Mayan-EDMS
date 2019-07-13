from __future__ import unicode_literals

import errno
import os

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .literals import BOOTSTRAP_SETTING_LIST


def get_default(name, fallback_default=None):
    for item in BOOTSTRAP_SETTING_LIST:
        if item['name'] == name:
            return item.get('default', fallback_default)

    return fallback_default


def get_environment_variables():
    result = {}

    for setting in BOOTSTRAP_SETTING_LIST:
        environment_value = os.environ.get('MAYAN_{}'.format(setting['name']))
        if environment_value:
            environment_value = yaml.load(stream=environment_value, Loader=SafeLoader)
            result[setting['name']] = environment_value

    return result


def get_environment_setting(name, fallback_default=None):
    value = os.environ.get('MAYAN_{}'.format(name), get_default(name=name, fallback_default=fallback_default))

    if value:
        return yaml.load(stream=value, Loader=SafeLoader)


def read_configuration_file(path):
    try:
        with open(path) as file_object:
            file_object.seek(0, os.SEEK_END)
            if file_object.tell():
                file_object.seek(0)
                try:
                    return yaml.load(stream=file_object, Loader=SafeLoader)
                except yaml.YAMLError as exception:
                    exit(
                        'Error loading configuration file: {}; {}'.format(
                            path, exception
                        )
                    )
    except IOError as exception:
        if exception.errno == errno.ENOENT:
            return {}  # No config file, return empty dictionary
        else:
            raise


def yaml_loads(data, error_message=None):
    if not error_message:
        error_message = 'Error loading: {}; {}'

    try:
        return yaml.load(stream=data, Loader=SafeLoader)
    except yaml.YAMLError as exception:
        exit(
            error_message.format(data, exception)
        )
