from django.core import management
from django.core.management.base import CommandError

from ...signals import signal_perform_upgrade, signal_post_upgrade, signal_pre_upgrade


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-dependencies', action='store_true', dest='no_dependencies',
            help='Don\'t download dependencies.',
        )

    def handle(self, *args, **options):
        try:
            signal_pre_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during signal_pre_upgrade signal: %s, %s' % (
                    exception, type(exception)
                )
            )

        if not options.get('no_dependencies', False):
            management.call_command(
                command_name='installdependencies'
            )
            management.call_command(
                command_name='preparestatic', interactive=False
            )

        try:
            signal_perform_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during signal_perform_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )

        try:
            signal_post_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error during signal_post_upgrade signal; %s, %s' % (
                    exception, type(exception)
                )
            )
