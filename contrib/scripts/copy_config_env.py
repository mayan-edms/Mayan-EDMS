#!/usr/bin/env python

import os
import sys


class ConfigEnvCopier:
    def __init__(self):
        sys.path.insert(1, os.path.abspath('.'))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')

    def copy(self):
        from mayan.apps.platform.utils import load_env_file

        result = load_env_file()

        for key, value in result.items():
            try:
                clean_value = int(value)
            except ValueError:
                clean_value = '\'{}\''.format(value)

            print('{} = {}'.format(key, clean_value))


if __name__ == '__main__':
    instance = ConfigEnvCopier()
    instance.copy()
