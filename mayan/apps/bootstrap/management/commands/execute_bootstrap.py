from __future__ import absolute_import

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ...models import BootstrapSetup
from ...exceptions import ExistingData


class Command(BaseCommand):
    help = 'Execute a bootstrap setup by the given slug.'
    args = '[bootstrap setup slug]'

    def handle(self, bootstrap_setup_slug=None, **options):
        if not bootstrap_setup_slug:
            raise CommandError('Enter one bootstrap setup slug.')

        # Get corresponding bootstrap setup instance
        try:
            bootstrap_setup = BootstrapSetup.objects.get(slug=bootstrap_setup_slug)
        except BootstrapSetup.DoesNotExist:
            raise CommandError('No bootstrap setup with such a slug.')

        # Try to execute bootstrap setup, catch errors
        try:
            bootstrap_setup.execute()
        except ExistingData:
            raise CommandError('Cannot execute bootstrap setup, there is existing data.  Erase all data and try again.')
        except Exception as exception:
            raise CommandError('Unhandled exception: %s' % exception)
