from __future__ import unicode_literals

from django.core import management

from ...models import Organization


class Command(management.BaseCommand):
    help = 'Creates an organization admin user with a secure random password and all permissions.'

    def handle(self, *args, **options):
        organization = Organization.objects.get_current()
        organization.create_admin()
