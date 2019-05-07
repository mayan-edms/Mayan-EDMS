from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)

from .literals import TEST_FILE_METADATA_KEY


@override_settings(FILE_METADATA_AUTO_PROCESS=True)
class FileMetadataViewsTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(FileMetadataViewsTestCase, self).setUp()
        self.test_driver = self.test_document.latest_version.file_metadata_drivers.first()

    def _request_document_version_driver_list_view(self):
        return self.get(
            viewname='file_metadata:document_driver_list',
            kwargs={'document_id': self.test_document.pk}
        )

    def test_document_version_driver_list_view_no_permission(self):
        response = self._request_document_version_driver_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_driver_list_view_with_access(self):
        self.grant_access(
            permission=permission_file_metadata_view, obj=self.test_document
        )

        response = self._request_document_version_driver_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def _request_document_version_file_metadata_list_view(self):
        return self.get(
            viewname='file_metadata:document_version_driver_file_metadata_list',
            kwargs={
                'document_version_driver_id': self.test_driver.pk
            }
        )

    def test_document_version_file_metadata_list_view_no_permission(self):
        response = self._request_document_version_file_metadata_list_view()
        self.assertNotContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=404
        )

    def test_document_version_file_metadata_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_file_metadata_view
        )

        response = self._request_document_version_file_metadata_list_view()
        self.assertContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=200
        )

    def _request_document_submit_view(self):
        return self.post(
            viewname='file_metadata:document_submit',
            kwargs={'document_id': self.test_document.pk}
        )

    def test_document_submit_view_no_permission(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()

        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_document_submit_view_with_access(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        response = self._request_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )

    def _request_multiple_document_submit_view(self):
        return self.post(
            viewname='file_metadata:document_multiple_submit',
            data={
                'id_list': self.test_document.pk,
            }
        )

    def test_multiple_document_submit_view_no_permission(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()

        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_multiple_document_submit_view_with_access(self):
        self.test_document.latest_version.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        response = self._request_multiple_document_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )


class DocumentTypeViewsTestCase(GenericDocumentViewTestCase):
    def _request_document_type_settings_view(self):
        return self.get(
            viewname='file_metadata:document_type_settings',
            kwargs={'document_type_id': self.test_document.document_type.pk}
        )

    def test_document_type_settings_view_no_permission(self):
        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 404)

    def test_document_type_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_file_metadata_setup
        )

        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 200)

    def _request_document_type_submit_view(self):
        return self.post(
            viewname='file_metadata:document_type_submit', data={
                'document_type': self.test_document_type.pk,
            }
        )

    def test_document_type_submit_view_no_permission(self):
        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 0
        )

    def test_document_type_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_file_metadata_submit
        )

        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.file_metadata_drivers.count(), 1
        )
