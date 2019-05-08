from __future__ import unicode_literals

from django.core import management
from django.core.management.base import CommandError

from ...signals import perform_upgrade, post_upgrade, pre_upgrade


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-javascript', action='store_true', dest='no_javascript',
            help='Don\'t download the JavaScript dependencies.',
        )

    def handle(self, *args, **options):
        try:
            pre_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during pre_upgrade signal: %s, %s' % (
                    exception, type(exception)
                )
            )

        if not options.get('no_javascript', False):
            management.call_command(
                command_name='installjavascript', interactive=False
            )

        try:
            perform_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during perform_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )

        try:
            post_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during post_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )
