from __future__ import absolute_import, unicode_literals

import os

from pathlib2 import Path

from django.conf import settings
from django.utils.encoding import force_text

from mayan.apps.common.settings import setting_paginate_by
from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.storage.utils import fs_cleanup

from ..classes import Setting

from .literals import ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE
from .mixins import SmartSettingTestMixin


class ClassesTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_environment_variable(self):
        os.environ[
            'MAYAN_{}'.format(ENVIRONMENT_TEST_NAME)
        ] = ENVIRONMENT_TEST_VALUE
        self.assertTrue(setting_paginate_by.value, ENVIRONMENT_TEST_VALUE)

    def test_config_backup_creation(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(filename=force_text(path_config_backup))

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

    def test_config_backup_creation_no_tags(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(filename=force_text(path_config_backup))

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

        with path_config_backup.open(mode='r') as file_object:
            self.assertFalse('!!python/' in file_object.read())

    def test_setting_check_changed(self):
        self._create_test_settings_namespace()
        test_setting = self.test_settings_namespace.add_setting(
            global_name='SMART_SETTINGS_TEST_SETTING',
            default='test value'
        )
        # Initialize hash cache
        Setting._cache_hash = None
        Setting.check_changed()
        self.assertFalse(Setting.check_changed())
        test_setting.value = 'test value edited'
        self.assertTrue(Setting.check_changed())
