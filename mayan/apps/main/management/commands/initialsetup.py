import os
import string
import random

from django.conf import settings
from django.core import management


class Command(management.BaseCommand):
    help = 'Gets Mayan EDMS ready to be used (initializes database, creates a secret key, etc).'

    def _generate_secret_key(self):
        return ''.join([random.SystemRandom().choice((string.digits + string.letters + string.punctuation).replace("'",'')) for i in range(100)])

    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'mayan', 'settings', 'local.py'), 'w+') as file_object:
            file_object.write('\n'.join([
                'from __future__ import absolute_import',
                'from .base import *',
                '',
                "SECRET_KEY = '{0}'".format(self._generate_secret_key()),
                '',
            ]))
        management.call_command('syncdb', migrate=True, interactive=False)
