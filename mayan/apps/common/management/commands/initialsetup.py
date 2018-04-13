from __future__ import unicode_literals

import os

from django.conf import settings
from django.core import management
from django.core.management.utils import get_random_secret_key

import mayan
from mayan.settings.literals import SECRET_KEY_FILENAME, SYSTEM_DIR

from ...signals import post_initial_setup, pre_initial_setup


class Command(management.BaseCommand):
    help = 'Initializes an install and gets it ready to be used.'

    def initialize_system(self):
        system_path = os.path.join(settings.MEDIA_ROOT, SYSTEM_DIR)
        secret_key_file_path = os.path.join(system_path, SECRET_KEY_FILENAME)

        if not os.path.exists(system_path):
            os.makedirs(system_path)

            version_file_path = os.path.join(system_path, 'VERSION')
            with open(version_file_path, 'w+') as file_object:
                file_object.write(mayan.__version__)

            with open(secret_key_file_path, 'w+') as file_object:
                secret_key = get_random_secret_key()
                file_object.write(secret_key)

            settings.SECRET_KEY = secret_key

    def handle(self, *args, **options):
        self.initialize_system()
        pre_initial_setup.send(sender=self)
        management.call_command('installjavascript', interactive=False)
        management.call_command('createautoadmin', interactive=False)
        post_initial_setup.send(sender=self)
