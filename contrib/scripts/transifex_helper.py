#!/usr/bin/env python

import configparser
import os
from pathlib import Path
import sys

import django
from django.apps import apps

from django.template import Template, Context
from django.utils.encoding import force_text

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(1, os.path.abspath('.'))

import mayan
from mayan.settings import BASE_DIR
from mayan.apps.common.apps import MayanAppConfig


class TransifexHelper:
    def __init__(self):
        django.setup()

    def get_app_list(self):
        return sorted(
            [
                name for name, app_config in apps.app_configs.items() if issubclass(type(app_config), MayanAppConfig)
            ]
        )

    def load_transifex_config(self):
        transifex_config = configparser.ConfigParser()
        transifex_config_path = Path(BASE_DIR, '..', '.tx', 'config')

        with transifex_config_path.open(mode='r') as file_object:
            transifex_config.read_file(file_object)

        return transifex_config

    def is_app_name_in_config(self, app_name):
        sections = self.load_transifex_config().sections()
        app_name_string = 'mayan-edms.{}'.format(app_name)
        for section in sections:
            if section.startswith(app_name_string):
                return True

        return False

    def find_missing_apps(self):
        sections = transifex_helper.load_transifex_config().sections()
        app_list = transifex_helper.get_app_list()

        missing_list = set()
        for app_name in app_list:
            if not transifex_helper.is_app_name_in_config(app_name=app_name):
                missing_list.add(app_name)

        return missing_list


if __name__ == '__main__':
    transifex_helper = TransifexHelper()

    missing_list = transifex_helper.find_missing_apps()
    if missing_list:
        print('Apps without a transifex entry: {}'.format(', '.join(missing_list)))
        exit(1)
    else:
        print('No missing apps')
