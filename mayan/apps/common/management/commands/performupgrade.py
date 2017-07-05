from __future__ import unicode_literals

from django.core import management
from django.core.management.base import CommandError

from ...signals import perform_upgrade, post_upgrade


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def handle(self, *args, **options):
        management.call_command('migrate', fake_initial=True, interactive=False)
        management.call_command('purgeperiodictasks', interactive=False)

        try:
            perform_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error executing upgrade task; %s' % exception
            )

        try:
            post_upgrade.send(sender=self)
        except Exception as exception:
            raise CommandError(
                'Error executing post-upgrade task; %s' % exception
            )



