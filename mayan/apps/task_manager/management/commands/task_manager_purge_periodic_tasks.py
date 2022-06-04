from django.core import management

from ...utils import purge_periodic_tasks


class Command(management.BaseCommand):
    help = 'Removes all periodic tasks.'

    def handle(self, *args, **options):
        purge_periodic_tasks()
