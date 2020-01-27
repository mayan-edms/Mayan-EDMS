from __future__ import unicode_literals

from django.core import management

import mayan


class Command(management.BaseCommand):
    help = 'Display version information.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--build-string', action='store_true', dest='build_string',
            help='Show build string.',
        )

    def handle(self, *args, **options):
        if options['build_string']:
            self.stdout.write(mayan.__build_string__ + '\n')
        else:
            self.stdout.write(mayan.__version__ + '\n')
