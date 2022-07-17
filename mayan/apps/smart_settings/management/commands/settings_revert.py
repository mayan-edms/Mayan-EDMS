from django.core import management

from ...classes import Setting


class Command(management.BaseCommand):
    help = 'Rollback the configuration file to the last valid version.'

    def handle(self, *args, **options):
        try:
            Setting.revert_configuration()
        except Exception as exception:
            self.stderr.write(
                msg=self.style.NOTICE(
                    str(exception)
                )
            )
            exit(1)
