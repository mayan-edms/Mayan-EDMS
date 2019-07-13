from __future__ import unicode_literals

from django.core import management
from django.utils.translation import ugettext_lazy as _

from ...classes import GoogleFontDependency, JavaScriptDependency


class Command(management.BaseCommand):
    help = 'Install JavaScript dependencies.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app', action='store', dest='app',
            help=_('Process a specific app.'),
        )
        parser.add_argument(
            '--force', action='store_true', dest='force',
            help=_('Force installation even if already installed.'),
        )

    def handle(self, *args, **options):
        JavaScriptDependency.install_multiple(
            app_label=options['app'], force=options['force'],
            subclass_only=True
        )
        GoogleFontDependency.install_multiple(
            app_label=options['app'], force=options['force'],
            subclass_only=True
        )
