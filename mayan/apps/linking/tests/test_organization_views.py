from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import SmartLink

from .literals import (
    TEST_SMART_LINK_DYNAMIC_LABEL, TEST_SMART_LINK_EDITED_LABEL,
    TEST_SMART_LINK_LABEL
)


class OrganizationIndexViewTestCase(OrganizationViewTestCase):
    def create_smart_link(self):
        self.smart_link = SmartLink.on_organization.create(
            organization=self.organization_a, label=TEST_SMART_LINK_LABEL
        )

    def test_smart_link_create_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.post(
                'linking:smart_link_create', data={
                    'label': TEST_SMART_LINK_LABEL
                }
            )
            self.assertEqual(SmartLink.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(SmartLink.on_organization.count(), 0)

    def test_smart_link_delete_view(self):
        self.create_smart_link()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'linking:smart_link_delete', args=(self.smart_link.pk,)
            )
            self.assertEqual(response.status_code, 404)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertEqual(SmartLink.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'linking:smart_link_delete', args=(self.smart_link.pk,)
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(SmartLink.on_organization.count(), 0)

    def test_smart_link_edit_view(self):
        self.create_smart_link()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'linking:smart_link_edit', args=(self.smart_link.pk,),
                data={
                    'label': TEST_SMART_LINK_EDITED_LABEL
                }
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(self.smart_link.label, TEST_SMART_LINK_LABEL)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'linking:smart_link_edit', args=(self.smart_link.pk,),
                data={
                    'label': TEST_SMART_LINK_EDITED_LABEL
                }
            )

            self.assertEqual(response.status_code, 302)
            self.smart_link.refresh_from_db()

            self.assertEqual(
                self.smart_link.label, TEST_SMART_LINK_EDITED_LABEL
            )

    def test_smart_link_list_view(self):
        self.create_smart_link()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get('linking:smart_link_list')

            self.assertNotContains(
                response, text=self.smart_link.label, status_code=200
            )

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get('linking:smart_link_list')

            self.assertContains(
                response, text=self.smart_link.label, status_code=200
            )
