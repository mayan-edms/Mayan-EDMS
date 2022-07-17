from pathlib import Path

from django.conf import settings
from django.core import management
from django.core.management.utils import get_random_secret_key

from mayan.settings.literals import (
    DEFAULT_USER_SETTINGS_FOLDER, SECRET_KEY_FILENAME, SYSTEM_DIR
)

from ..exceptions import BaseCommonException
from ..signals import (
    signal_perform_upgrade, signal_pre_initial_setup, signal_pre_upgrade,
    signal_post_initial_setup, signal_post_upgrade
)


class CommonAppManagementCommand:
    def __init__(self):
        self.path_media_root = Path(settings.MEDIA_ROOT)

        self.path_system = self.path_media_root / SYSTEM_DIR

        self.path_secret_key = self.path_system / SECRET_KEY_FILENAME

        self.path_user_settings = self.path_media_root / DEFAULT_USER_SETTINGS_FOLDER

    def do_create_user_settings_folder(self):
        self.path_user_settings.mkdir(exist_ok=True)

        # Touch media/settings/__init__.py
        (self.path_user_settings / '__init__.py').touch()

    def do_initial_setup(self, force=False, no_dependencies=False):
        # Create the media folder.
        try:
            self.path_media_root.mkdir()
        except FileExistsError as exception:
            if not force:
                raise BaseCommonException(
                    'Existing media files. Backup, remove this folder, '
                    'and try again. Or use the --force argument.'
                ) from exception

        # Touch media/__init__.py
        (self.path_media_root / '__init__.py').touch()

        self.do_create_user_settings_folder()

        # Create the media/system folder.
        try:
            self.path_system.mkdir()
        except FileExistsError as exception:
            if not force:
                raise BaseCommonException(
                    'System folder already exists.'
                ) from exception

        with self.path_secret_key.open(mode='w') as file_object:
            secret_key = get_random_secret_key()
            file_object.write(secret_key)

        settings.SECRET_KEY = secret_key

        signal_pre_initial_setup.send(sender=self)

        if not no_dependencies:
            self.do_install_dependencies()

        management.call_command(command_name='createautoadmin')
        management.call_command(command_name='savesettings')
        signal_post_initial_setup.send(sender=self)

    def do_install_dependencies(self):
        management.call_command(command_name='dependencies_install')
        management.call_command(
            command_name='appearance_prepare_static', interactive=False
        )

    def do_perform_upgrade(self, no_dependencies=False):
        try:
            signal_pre_upgrade.send(sender=self)
        except Exception as exception:
            raise BaseCommonException(
                'Error during signal_pre_upgrade signal.'
            ) from exception
        else:
            try:
                self.do_create_user_settings_folder()
            except FileExistsError:
                """
                This exception is expected when upgrading from recent version
                that already have a user settings folder.
                """
            else:
                if not no_dependencies:
                    self.do_install_dependencies()

                try:
                    signal_perform_upgrade.send(sender=self)
                except Exception as exception:
                    raise BaseCommonException(
                        'Error during signal_perform_upgrade signal.'
                    ) from exception
                else:
                    try:
                        signal_post_upgrade.send(sender=self)
                    except Exception as exception:
                        raise BaseCommonException(
                            'Error during signal_post_upgrade signal.'
                        ) from exception
