from django.core.management.base import BaseCommand

from ...classes import SearchBackend


class Command(BaseCommand):
    help = 'Initialize the search backend.'

    def handle(self, *args, **options):
        backend = SearchBackend.get_instance()

        backend.initialize()
