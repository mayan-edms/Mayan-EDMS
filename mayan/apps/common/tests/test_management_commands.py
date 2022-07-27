from pathlib import Path
from unittest import skip

from django.core import management
from django.test import override_settings

from mayan.apps.storage.utils import TemporaryDirectory
from mayan.apps.testing.tests.base import BaseTransactionTestCase
from mayan.apps.testing.tests.utils import mute_stdout
from mayan.settings.literals import (
    DEFAULT_USER_SETTINGS_FOLDER, SECRET_KEY_FILENAME, SYSTEM_DIR
)


@skip('Skip until existing database persistence with transaction handling is achieve.')
class CommonAppManagementCommandTestCase(BaseTransactionTestCase):
    def _call_command_initial_setup(self):
        options = {
            'no_dependencies': True
        }

        with mute_stdout():
            management.call_command(
                command_name='common_initial_setup', **options
            )

    def _call_command_perform_upgrade(self):
        options = {
            'no_dependencies': True
        }

        with mute_stdout():
            management.call_command(
                command_name='common_perform_upgrade', **options
            )

    def test_command_initial_setup_no_files(self):
        with TemporaryDirectory() as path_name:
            path_temporary_media = Path(path_name, 'media')
            with override_settings(MEDIA_ROOT=str(path_temporary_media)):
                self._call_command_initial_setup()

            self.assertTrue(
                (path_temporary_media / SYSTEM_DIR).exists()
            )
            self.assertTrue(
                (
                    path_temporary_media / SYSTEM_DIR / SECRET_KEY_FILENAME
                ).exists()
            )
            self.assertTrue(
                (
                    path_temporary_media / DEFAULT_USER_SETTINGS_FOLDER
                ).exists()
            )
            self.assertTrue(
                (
                    path_temporary_media / DEFAULT_USER_SETTINGS_FOLDER / '__init__.py'
                ).exists()
            )

    def test_command_initial_setup_existing_files(self):
        with TemporaryDirectory() as path_name:
            path_temporary_media = Path(path_name, 'media')
            with override_settings(MEDIA_ROOT=str(path_temporary_media)):
                self._call_command_initial_setup()
                with self.assertRaises(expected_exception=SystemExit):
                    self._call_command_initial_setup()

    def test_command_perform_upgrade_no_files(self):
        with TemporaryDirectory() as path_name:
            path_temporary_media = Path(path_name, 'media')
            with override_settings(MEDIA_ROOT=str(path_temporary_media)):
                with self.assertRaises(expected_exception=FileNotFoundError):
                    self._call_command_perform_upgrade()

    def test_command_perform_upgrade_existing_files(self):
        with TemporaryDirectory() as path_name:
            path_temporary_media = Path(path_name, 'media')
            with override_settings(MEDIA_ROOT=str(path_temporary_media)):
                self._call_command_initial_setup()
                self._call_command_perform_upgrade()
