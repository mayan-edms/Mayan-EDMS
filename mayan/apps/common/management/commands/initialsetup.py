from __future__ import unicode_literals

from django.core import management
from django.db.utils import OperationalError

from ...signals import post_initial_setup


class Command(management.BaseCommand):
    help = 'Initializes an install and gets it ready to be used.'

    def handle(self, *args, **options):
        management.call_command('createsettings', interactive=False)
        try:
            management.call_command('migrate', interactive=False)
        except OperationalError:
            self.stderr.write(
                self.style.NOTICE(
                    'Unable to migrate the database. The initialsetup '
                    'command is to be used only on new installations. To '
                    'upgrade existing installations use the performupgrade '
                    'command.'
                )
            )
            raise
        management.call_command('createautoadmin', interactive=False)
        post_initial_setup.send(sender=self)
