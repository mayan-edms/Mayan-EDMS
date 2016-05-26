from __future__ import absolute_import, unicode_literals

from documents.tests.test_views import GenericDocumentViewTestCase
from organizations.models import Organization

from ..models import Folder
from .literals import TEST_FOLDER_LABEL, TEST_FOLDER_EDITED_LABEL


class FolderOrganizationViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(FolderOrganizationViewTestCase, self).setUp()
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

    def test_folder_view_view(self):
        # Create a folder for organization A
        folder = Folder.objects.create(
            organization=self.organization_a, label=TEST_FOLDER_LABEL
        )

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot find the folder for
            # organization A
            response = self.get(
                'folders:folder_view', args=(folder.pk,),
            )
            self.assertEqual(response.status_code, 404)
