from __future__ import unicode_literals

from django.core import management

from ...classes import Setting


class Command(management.BaseCommand):
    help = 'Save the current settings into the configuration file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filepath', action='store', dest='filepath',
            help='Filename and path where to save the configuration file.'
        )

    def handle(self, *args, **options):
        Setting.save_configuration(path=options.get('filepath'))
