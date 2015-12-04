from __future__ import unicode_literals

from optparse import make_option

from django import apps
from django.core import management


class Command(management.BaseCommand):
    help = 'Run all configured tests for the project.'

    option_list = management.BaseCommand.option_list + (
        make_option(
            '--nomigrations', action='store_true', dest='nomigrations',
            default=False,
            help='Don\'t use migrations when creating the test database.'
        ),
    )

    def handle(self, *args, **options):
        kwargs = {}
        if options.get('nomigrations'):
            kwargs['nomigrations'] = True

        test_apps = [app.name for app in apps.apps.get_app_configs() if getattr(app, 'test', False)]

        print 'Testing: {}'.format(', '.join(test_apps))

        management.call_command('test', *test_apps, interactive=False, **kwargs)
