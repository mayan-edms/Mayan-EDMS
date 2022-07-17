from django.core import management

from ..base import CommonAppManagementCommand


class Command(management.BaseCommand):
    help = 'Initializes an install and gets it ready to be used.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true', dest='force',
            help='Force execution of the initialization process.',
        )
        parser.add_argument(
            '--no-dependencies', action='store_true', dest='no_dependencies',
            help='Don\'t download dependencies.',
        )

    def handle(self, *args, **options):
        instance = CommonAppManagementCommand()

        try:
            instance.do_initial_setup(
                force=options.get('force', False),
                no_dependencies=options.get('no_dependencies', False)
            )
        except Exception as exception:
            self.stderr.write(
                msg=self.style.NOTICE(
                    str(exception)
                )
            )
            exit(1)
