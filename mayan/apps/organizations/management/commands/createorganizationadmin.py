from __future__ import unicode_literals

import os

from django.conf import settings
from django.core import management
from django.utils.crypto import get_random_string

from ...models import Organization



class Command(management.BaseCommand):
    help = 'Creates an organization admin user with a secure random password and all permissions.'

    def handle(self, *args, **options):
        organization = Organization.objects.get_current()
        organization.create_admin()
