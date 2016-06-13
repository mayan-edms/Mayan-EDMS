from __future__ import absolute_import, unicode_literals

from common.tests.test_views import GenericViewTestCase

from ..models import Organization


class OrganizationViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(OrganizationViewTestCase, self).setUp()
        # Create two organizations
        self.organization_a = Organization.objects.create(
            label='Organization A'
        )
        self.organization_b = Organization.objects.create(
            label='Organization B'
        )

        # Create an organization admin for organization B
        user, password = self.organization_b.create_admin()
        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Login organization admin for organization B
            self.login(username=user.username, password=password)
