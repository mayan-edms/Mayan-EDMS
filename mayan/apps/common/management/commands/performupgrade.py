from __future__ import unicode_literals

from django.core import management

from ...signals import perform_upgrade, post_upgrade


class Command(management.BaseCommand):
    help = 'Performs the required steps after a version upgrade.'

    def handle(self, *args, **options):
        management.call_command('migrate', interactive=False)
        management.call_command('purgeperiodictasks', interactive=False)
        perform_upgrade.send(sender=self)
        post_upgrade.send(sender=self)
