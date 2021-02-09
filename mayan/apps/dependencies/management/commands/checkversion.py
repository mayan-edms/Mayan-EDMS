from django.core import management

from ...utils import PyPIClient


class Command(management.BaseCommand):
    help = 'Check if the current version is the latest.'

    def handle(self, *args, **options):
        self.stdout.write(
            '{}\n'.format(PyPIClient().check_version_verbose())
        )
