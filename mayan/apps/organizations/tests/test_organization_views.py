from __future__ import absolute_import, unicode_literals

from documents.tests.test_views import GenericDocumentViewTestCase

from ..models import Organization


class OrganizationViewTestCase(GenericDocumentViewTestCase):
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
        username, password = self.organization_b.create_admin()
        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Login organization admin for organization B
            self.login(username=username, password=password)
