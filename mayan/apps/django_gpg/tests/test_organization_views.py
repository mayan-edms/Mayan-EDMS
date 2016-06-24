from __future__ import unicode_literals

from django.test import override_settings

from django_downloadview.test import assert_download_response

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Key

from .literals import TEST_KEY_DATA, TEST_KEY_FINGERPRINT


@override_settings(OCR_AUTO_OCR=False)
class OrganizationKeyViewsTestCase(OrganizationViewTestCase):
    def create_key(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.key = Key.on_organization.create(key_data=TEST_KEY_DATA)

    def test_key_delete_view(self):
        self.create_key()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'django_gpg:key_delete',
                args=(self.key.pk,), follow=True
            )
            self.assertEqual(response.status_code, 404)

    def test_key_download_view(self):
        self.create_key()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(
                viewname='django_gpg:key_download', args=(self.key.pk,)
            )

            self.assertEqual(response.status_code, 404)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get(
                viewname='django_gpg:key_download', args=(self.key.pk,)
            )

            assert_download_response(
                self, response=response, content=self.key.key_data,
                basename=self.key.key_id,
            )

    def test_key_upload_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                viewname='django_gpg:key_upload',
                data={'key_data': TEST_KEY_DATA}, follow=True
            )
            self.assertContains(response, 'created', status_code=200)
            self.assertEqual(Key.on_organization.count(), 1)
            self.assertEqual(
                Key.on_organization.first().fingerprint, TEST_KEY_FINGERPRINT
            )

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(Key.on_organization.count(), 0)

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.assertEqual(Key.on_organization.count(), 1)

    def test_key_private_list_view(self):
        self.create_key()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(viewname='django_gpg:key_private_list')

            self.assertNotContains(
                response, text=self.key.key_id, status_code=200
            )

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get(viewname='django_gpg:key_private_list')

            self.assertContains(
                response, text=self.key.key_id, status_code=200
            )
