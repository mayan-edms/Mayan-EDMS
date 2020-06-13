from django.core import management

from ...backends.base import LockingBackend


class Command(management.BaseCommand):
    help = 'Erase all locks (acquired and stale).'

    def handle(self, *args, **options):
        LockingBackend.get_instance().purge_locks()
