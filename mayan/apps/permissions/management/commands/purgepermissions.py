from django.core.management.base import BaseCommand

from ...models import StoredPermission


class Command(BaseCommand):
    help = 'Remove obsolete permissions from the database'

    def handle(self, *args, **options):
        StoredPermission.objects.purge_obsolete()
