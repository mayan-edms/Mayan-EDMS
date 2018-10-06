from __future__ import unicode_literals

import errno
import os

import yaml


def read_configuration_file(path):
    try:
        with open(path) as file_object:
            file_object.seek(0, os.SEEK_END)
            if file_object.tell():
                file_object.seek(0)
                try:
                    return yaml.safe_load(file_object)
                except yaml.YAMLError as exception:
                    exit(
                        'Error loading configuration file: {}; {}'.format(
                            path, exception
                        )
                    )
    except IOError as exception:
        if exception.errno == errno.ENOENT:
            pass
        else:
            raise


def yaml_loads(data, error_message=None):
    if not error_message:
        error_message = 'Error loading: {}; {}'

    try:
        return yaml.safe_load(data)
    except yaml.YAMLError as exception:
        exit(
            error_message.format(data, exception)
        )
