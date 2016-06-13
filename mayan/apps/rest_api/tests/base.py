from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import override_settings

from rest_framework.test import APITestCase

from organizations.models import Organization
from organizations.utils import create_default_organization
from permissions.models import Role


class GenericAPITestCase(APITestCase):
    def setUp(self):
        super(GenericAPITestCase, self).setUp()

        self.organization = create_default_organization()

        # Create an organization admin
        self.admin_user, password = self.organization.create_admin()
        with self.settings(ORGANIZATION_ID=self.organization.pk):
            # Login organization admin
            self.client.login(
                username=self.admin_user.username, password=password
            )


    def tearDown(self):
        super(GenericAPITestCase, self).tearDown()
        self.admin_user.delete()
        Role.objects.all().delete()
        self.organization.delete()
        Organization.objects.clear_cache()
