from __future__ import unicode_literals

from django.core import management
from django.utils.translation import ugettext_lazy as _

from ...javascript import JSDependencyManager


class Command(management.BaseCommand):
    help = 'Install JavaScript dependencies.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app', action='store', dest='app',
            help=_('Process a specific app.'),
        )

    def handle(self, *args, **options):
        js_manager = JSDependencyManager()
        js_manager.install(app_name=options['app'])
