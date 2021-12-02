import errno
import os

from django.conf import settings
from django.core import management

from mayan.settings.literals import DEFAULT_USER_SETTINGS_FOLDER
from mayan.apps.storage.utils import touch

from ...signals import signal_perform_upgrade, signal_post_upgrade, signal_pre_upgrade


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-dependencies', action='store_true', dest='no_dependencies',
            help='Don\'t download dependencies.',
        )

    def handle(self, *args, **options):
        settings_path = os.path.join(
            settings.MEDIA_ROOT, DEFAULT_USER_SETTINGS_FOLDER
        )

        try:
            signal_pre_upgrade.send(sender=self)
        except Exception as exception:
            self.stderr.write(
                'Error during signal_pre_upgrade signal: %s, %s' % (
                    exception, type(exception)
                )
            )
            raise

        # Create user settings folder
        try:
            os.makedirs(name=settings_path)
        except OSError as exception:
            if exception.errno == errno.EEXIST:
                """Folder already exists. Ignore."""
            else:
                raise

        # Touch media/settings/__init__.py
        touch(filename=os.path.join(settings_path, '__init__.py'))

        if not options.get('no_dependencies', False):
            management.call_command(
                command_name='installdependencies'
            )
            management.call_command(
                command_name='preparestatic', interactive=False
            )

        try:
            signal_perform_upgrade.send(sender=self)
        except Exception as exception:
            self.stderr.write(
                'Error during signal_perform_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )
            raise

        try:
            signal_post_upgrade.send(sender=self)
        except Exception as exception:
            self.stderr.write(
                'Error during signal_post_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )
            raise
