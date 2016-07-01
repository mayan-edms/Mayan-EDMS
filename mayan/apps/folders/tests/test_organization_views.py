from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Folder

from .literals import TEST_FOLDER_LABEL, TEST_FOLDER_EDITED_LABEL


class FolderOrganizationViewTestCase(OrganizationViewTestCase):
    def test_folder_create_view(self):
        # Create a folder for organization A
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.post(
                'folders:folder_create', data={
                    'label': TEST_FOLDER_LABEL
                }
            )
            self.assertEqual(Folder.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(Folder.on_organization.count(), 0)

    def test_folder_delete_view(self):
        # Create a folder for organization A
        folder = Folder.objects.create(
            organization=self.organization_a, label=TEST_FOLDER_LABEL
        )

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post('folders:folder_delete', args=(folder.pk,))
            self.assertEqual(response.status_code, 404)

    def test_folder_edit_view(self):
        # Create a folder for organization A
        folder = Folder.objects.create(
            organization=self.organization_a, label=TEST_FOLDER_LABEL
        )

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot edit the folder
            response = self.post(
                'folders:folder_edit', args=(folder.pk,), data={
                    'label': TEST_FOLDER_EDITED_LABEL
                }
            )

            self.assertEqual(response.status_code, 404)

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
