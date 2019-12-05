from __future__ import unicode_literals

from django.conf import settings
from django.utils.encoding import force_bytes

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.common.tests.mixins import EnvironmentTestCaseMixin
from mayan.apps.smart_settings.classes import Setting
from mayan.apps.storage.utils import NamedTemporaryFile

from ..settings import setting_drivers_arguments


class FileMetadataSettingMigrationTestCase(
    EnvironmentTestCaseMixin, BaseTestCase
):
    def test_file_metadata_drivers_arguments_0001_migration(self):

        test_value = {'location': 'test value'}

        with NamedTemporaryFile() as file_object:
            settings.CONFIGURATION_FILEPATH = file_object.name
            file_object.write(
                force_bytes(
                    '{}: {}'.format(
                        'FILE_METADATA_DRIVERS_ARGUMENTS',
                        '"{}"'.format(
                            Setting.serialize_value(value=test_value)
                        )
                    )
                )
            )
            file_object.seek(0)
            Setting._config_file_cache = None

            self.assertEqual(
                setting_drivers_arguments.value,
                test_value
            )
