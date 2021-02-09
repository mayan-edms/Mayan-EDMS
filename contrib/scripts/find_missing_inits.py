#!/usr/bin/env python

import os
from pathlib import Path
import re
import sys

import django
from django.conf import settings

EXCLUSIONS = r'bin|node_modules'


class InitScanner:
    def __init__(self, exclusions=None):
        self.hits = 0

        if exclusions:
            self.regex_pattern = re.compile(pattern=exclusions)
        else:
            self.regex_pattern = None

    def check_folder(self, folder_string=None):
        folder = Path(folder_string)

        for child in folder.iterdir():
            if child.is_dir():
                self.check_folder(folder_string=str(child))

        if self.regex_pattern and self.regex_pattern.findall(string=str(folder)):
            return

        python_files = list(folder.glob(pattern='*.py'))
        names = [python_file.name for python_file in python_files]
        if len(names) > 0 and '__init__.py' not in names:
            print('folder: {}; {}'.format(folder, ', '.join(names)))
            self.hits += 1


if __name__ == '__main__':
    sys.path.insert(1, os.path.abspath('.'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')

    django.setup()

    init_scanner = InitScanner(exclusions=EXCLUSIONS)
    init_scanner.check_folder(folder_string=settings.BASE_DIR)
    if init_scanner.hits:
        exit(1)
