from __future__ import unicode_literals

import os

from django.conf import settings
from django.core import management
from django.utils.crypto import get_random_string


class Command(management.BaseCommand):
    help = 'Creates a local settings file with a random secret key.'

    @staticmethod
    def _generate_secret_key():
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return get_random_string(50, chars)

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'mayan', 'settings', 'local.py')
        if os.path.exists(path):
            print 'Existing file at: {0}. Backup, remove this file and try again.'.format(path)
        else:
            with open(path, 'w+') as file_object:
                file_object.write('\n'.join([
                    'from __future__ import absolute_import',
                    '',
                    'from .base import *',
                    '',
                    "SECRET_KEY = '{0}'".format(Command._generate_secret_key()),
                    '',
                ]))
