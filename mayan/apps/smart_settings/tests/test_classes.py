from __future__ import absolute_import, unicode_literals

import os

from pathlib2 import Path

from django.conf import settings

from mayan.apps.common.settings import setting_paginate_by
from mayan.apps.common.tests import BaseTestCase

from ..classes import Setting

from .literals import ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE


class ClassesTestCase(BaseTestCase):
    def test_environment_variable(self):
        os.environ[
            'MAYAN_{}'.format(ENVIRONMENT_TEST_NAME)
        ] = ENVIRONMENT_TEST_VALUE
        self.assertTrue(setting_paginate_by.value, ENVIRONMENT_TEST_VALUE)

    def test_config_backup_creation(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        path_config_backup.unlink()

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

    def test_config_backup_creation_no_tags(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        path_config_backup.unlink()

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

        with path_config_backup.open(mode='r') as file_object:
            self.assertFalse('!!python/' in file_object.read())
