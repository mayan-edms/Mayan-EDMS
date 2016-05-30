from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import WebFormSource

from .literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_EDITED_LABEL, TEST_SOURCE_UNCOMPRESS_N
)


class SourceOrganizationViewTestCase(OrganizationViewTestCase):
    def create_source(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.source = WebFormSource.on_organization.create(
                enabled=True, label=TEST_SOURCE_LABEL,
                uncompress=TEST_SOURCE_UNCOMPRESS_N
            )

    def test_source_create_view(self):
        # Create a source for organization A
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'sources:setup_source_create',
                args=(WebFormSource.source_type,), data={
                    'label': TEST_SOURCE_LABEL,
                    'uncompress': TEST_SOURCE_UNCOMPRESS_N
                }
            )
            self.assertNotContains(response, text='danger', status_code=302)
            self.assertEqual(WebFormSource.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(WebFormSource.on_organization.count(), 0)

    def test_source_delete_view(self):
        self.create_source()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'sources:setup_source_delete', args=(self.source.pk,)
            )
            self.assertEqual(response.status_code, 404)

    def test_source_edit_view(self):
        self.create_source()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot edit the source
            response = self.post(
                'sources:setup_source_edit', args=(self.source.pk,), data={
                    'label': TEST_SOURCE_EDITED_LABEL
                }
            )

            self.assertEqual(response.status_code, 404)

    def test_source_list_view(self):
        self.create_source()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot find the source for
            # organization A
            response = self.get(
                'sources:setup_source_list',
            )

            self.assertNotContains(
                response, text=self.source.label, status_code=200
            )
