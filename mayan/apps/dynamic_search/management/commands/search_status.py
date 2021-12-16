from django.core.management.base import BaseCommand

from ...classes import SearchBackend


class Command(BaseCommand):
    help = 'Show search backend statistics.'

    def handle(self, *args, **options):
        backend = SearchBackend.get_instance()

        result = backend.get_status()

        self.stdout.write(msg=result)
