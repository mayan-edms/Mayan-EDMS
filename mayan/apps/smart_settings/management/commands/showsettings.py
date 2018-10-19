from __future__ import unicode_literals

from django.core import management

from ...classes import Setting


class Command(management.BaseCommand):
    help = 'Display the current settings.'

    def add_arguments(self, parser):

        parser.add_argument(
            dest='filter_term', nargs='?', help='Use this term to filter the '
            'list of settings.'
        )

        parser.add_argument(
            '--namespace', action='store', dest='namespace',
            help='Name (not label) of the namespace for which to filter the '
            'list of settings. Names are lowercase with words separated by '
            'underscore.'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            Setting.dump_data(
                namespace=options.get('namespace'),
                filter_term=options.get('filter_term')
            )
        )
