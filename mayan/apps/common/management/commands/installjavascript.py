from __future__ import unicode_literals

from django.core import management

from ...javascript import JSDependencyManager


class Command(management.BaseCommand):
    help = 'Install JavaScript dependencies.'

    def handle(self, *args, **options):
        js_manager = JSDependencyManager()
        js_manager.install()
