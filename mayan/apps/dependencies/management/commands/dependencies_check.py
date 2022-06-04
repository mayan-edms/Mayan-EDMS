from django.core import management
from django.utils.translation import ugettext_lazy as _

from ...classes import Dependency


class Command(management.BaseCommand):
    help = 'Output the status of the defined dependencies.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv', action='store_true', dest='csv', help=_(
                'Outputs the dependencies as a comma delimited values list.'
            ),
        )

    def handle(self, *args, **options):
        Dependency.check_all(as_csv=options['csv'], use_color=True)
