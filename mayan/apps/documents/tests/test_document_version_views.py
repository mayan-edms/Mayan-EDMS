from mayan.apps.file_caching.models import CachePartitionFile
from mayan.apps.file_caching.permissions import permission_cache_partition_purge
from mayan.apps.file_caching.tests.mixins import CachePartitionViewTestMixin
from mayan.apps.storage.models import DownloadFile
from mayan.apps.testing.tests.mixins import ContentTypeTestCaseMixin

from ..permissions import (
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_print, permission_document_version_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_version_mixins import (
    DocumentVersionTestMixin, DocumentVersionViewTestMixin
)


class DocumentVersionViewTestCase(
    DocumentVersionTestMixin, DocumentVersionViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_version_active_view_no_permission(self):
        self._create_test_document_version()

        self.test_document.versions.first().active_set()

        response = self._request_test_document_version_active_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()
        self.assertFalse(self.test_document_version.active)

    def test_document_version_active_view_with_access(self):
        self._create_test_document_version()

        self.test_document.versions.first().active_set()

        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_active_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()
        self.assertTrue(self.test_document_version.active)

    def test_document_version_edit_view_no_permission(self):
        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()
        self.assertEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_edit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_export_view_no_permission(self):
        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

    def test_document_version_export_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_export
        )

        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

    def test_document_version_list_view_no_permission(self):
        response = self._request_test_document_version_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )

    def test_document_version_preview_view_no_permission(self):
        response = self._request_test_document_version_preview_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_preview_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )

    def test_document_version_print_form_view_no_permission(self):
        response = self._request_test_document_version_print_form_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_print_form_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_print
        )

        response = self._request_test_document_version_print_form_view()
        self.assertEqual(response.status_code, 200)

    def test_document_version_print_view_no_permission(self):
        response = self._request_test_document_version_print_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_print_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_print
        )

        response = self._request_test_document_version_print_view()
        self.assertEqual(response.status_code, 200)


class DocumentVersionCachePurgeViewTestCase(
    CachePartitionViewTestMixin, ContentTypeTestCaseMixin,
    GenericDocumentViewTestCase
):
    def test_document_version_cache_purge_no_permission(self):
        self.test_object = self.test_document_version
        self._inject_test_object_content_type()

        self.test_document_version.version_pages.first().generate_image()

        test_document_version_cache_partitions = self.test_document_version.get_cache_partitions()

        cache_partition_version_count = CachePartitionFile.objects.filter(
            partition__in=test_document_version_cache_partitions
        ).count()

        response = self._request_test_object_file_cache_partition_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            CachePartitionFile.objects.filter(
                partition__in=test_document_version_cache_partitions
            ).count(), cache_partition_version_count
        )

    def test_document_version_cache_purge_with_access(self):
        self.test_object = self.test_document_version
        self._inject_test_object_content_type()

        self.grant_access(
            obj=self.test_document_version,
            permission=permission_cache_partition_purge
        )

        self.test_document_version.version_pages.first().generate_image()

        test_document_version_cache_partitions = self.test_document_version.get_cache_partitions()

        cache_partition_version_count = CachePartitionFile.objects.filter(
            partition__in=test_document_version_cache_partitions
        ).count()

        response = self._request_test_object_file_cache_partition_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            CachePartitionFile.objects.filter(
                partition__in=test_document_version_cache_partitions
            ).count(), cache_partition_version_count
        )
