from django.core import management

from ...classes import Dependency


class Command(management.BaseCommand):
    help = 'Output the status of the defined dependencies.'

    def handle(self, *args, **options):
        Dependency.check_all()
