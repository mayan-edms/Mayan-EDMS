from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import MetadataType

from .literals import (
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_2,
    TEST_METADATA_TYPE_NAME,
)


class MetadataOrganizationViewTestCase(OrganizationViewTestCase):
    def create_metadata_type(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.metadata_type = MetadataType.on_organization.create(
                name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
            )

    def test_metadata_type_creation(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'metadata:setup_metadata_type_create', data={
                    'label': TEST_METADATA_TYPE_LABEL,
                    'name': TEST_METADATA_TYPE_NAME
                }, follow=True
            )

        self.assertContains(response, text='created', status_code=200)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(MetadataType.on_organization.count(), 0)

    def test_metadata_type_delete(self):
        self.create_metadata_type()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'metadata:setup_metadata_type_delete',
                args=(self.metadata_type.pk,), follow=True
            )

            self.assertEqual(response.status_code, 404)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertEqual(MetadataType.on_organization.count(), 1)

    def test_metadata_type_edit(self):
        self.create_metadata_type()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'metadata:setup_metadata_type_edit',
                args=(self.metadata_type.pk,), data={
                    'label': TEST_METADATA_TYPE_LABEL_2,
                }
            )
            self.assertEqual(response.status_code, 404)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.metadata_type.refresh_from_db()
            self.assertEqual(
                self.metadata_type.label, TEST_METADATA_TYPE_LABEL
            )
