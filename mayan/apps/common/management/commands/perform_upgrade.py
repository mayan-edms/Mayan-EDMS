from django.core import management

from ..base import CommonAppManagementCommand


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-dependencies', action='store_true', dest='no_dependencies',
            help='Don\'t download dependencies.',
        )

    def handle(self, *args, **options):
        instance = CommonAppManagementCommand()

        instance.do_perform_upgrade(
            no_dependencies=options.get('no_dependencies', False)
        )
