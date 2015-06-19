from __future__ import unicode_literals

import os

from django.conf import settings
from django.core import management
from django.utils.crypto import get_random_string

from ...signals import post_initial_setup


class Command(management.BaseCommand):
    help = 'Gets Mayan EDMS ready to be used (initializes database, creates a secret key, etc).'

    @staticmethod
    def _generate_secret_key():
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return get_random_string(50, chars)

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'mayan', 'settings', 'local.py')
        if os.path.exists(path):
            print 'Existing file at: {0}. Backup, remove this file and try again.'.format(path)
            exit(1)

        with open(path, 'w+') as file_object:
            file_object.write('\n'.join([
                'from __future__ import absolute_import',
                '',
                'from .base import *',
                '',
                "SECRET_KEY = '{0}'".format(Command._generate_secret_key()),
                '',
            ]))
        management.call_command('migrate', interactive=False)
        management.call_command('createautoadmin', interactive=False)
        post_initial_setup.send(sender=self)
