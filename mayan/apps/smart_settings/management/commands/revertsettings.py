import errno
from shutil import copyfile

from django.conf import settings
from django.core import management


class Command(management.BaseCommand):
    help = 'Rollback the configuration file to the last valid version.'

    def handle(self, *args, **options):
        try:
            copyfile(
                settings.CONFIGURATION_LAST_GOOD_FILEPATH,
                settings.CONFIGURATION_FILEPATH
            )
        except IOError as exception:
            if exception.errno == errno.ENOENT:
                self.stdout.write(
                    self.style.NOTICE(
                        'There is no last valid version to restore.'
                    )
                )
            else:
                raise
