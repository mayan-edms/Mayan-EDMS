from django.core.management.base import BaseCommand

from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Generate a random value that is valid for use as a SECRET_KEY.'

    def handle(self, *args, **options):
        self.stdout.write(msg=get_random_secret_key())
