from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.converter.tests.mixins import LayerTestMixin
from mayan.apps.documents.tests.literals import TEST_MULTI_PAGE_TIFF
from mayan.apps.file_caching.models import CachePartitionFile
from mayan.apps.file_caching.permissions import permission_cache_partition_purge
from mayan.apps.file_caching.tests.mixins import CachePartitionViewTestMixin
from mayan.apps.testing.tests.mixins import ContentTypeTestCaseMixin

from ..events import event_document_file_downloaded
from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_edit, permission_document_file_print,
    permission_document_file_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_file_mixins import (
    DocumentFileTestMixin, DocumentFileTransformationTestMixin,
    DocumentFileTransformationViewTestMixin, DocumentFileViewTestMixin
)


class DocumentFileViewTestCase(
    DocumentFileTestMixin, DocumentFileViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_delete_no_permission(self):
        first_file = self.test_document.file_latest
        self._upload_new_file()

        response = self._request_test_document_file_delete_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.files.count(), 2)

    def test_document_file_delete_with_access(self):
        first_file = self.test_document.file_latest
        self._upload_new_file()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_delete
        )

        response = self._request_test_document_file_delete_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.files.count(), 1)

    def test_document_file_edit_view_no_permission(self):
        document_file_comment = self.test_document_file.comment

        response = self._request_test_document_file_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_file.refresh_from_db()
        self.assertEqual(
            self.test_document_file.comment,
            document_file_comment
        )

    def test_document_file_edit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_edit
        )

        document_file_comment = self.test_document_file.comment
        document_file_filename = self.test_document_file.filename

        response = self._request_test_document_file_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_file.refresh_from_db()
        self.assertNotEqual(
            self.test_document_file.comment,
            document_file_comment
        )
        self.assertNotEqual(
            self.test_document_file.filename,
            document_file_filename
        )

    def test_document_file_list_no_permission(self):
        response = self._request_test_document_file_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_list_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        response = self._request_test_document_file_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_file)
        )

    def test_document_file_print_form_view_no_permission(self):
        response = self._request_test_document_file_print_form_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_print_form_view_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_print
        )

        response = self._request_test_document_file_print_form_view()
        self.assertEqual(response.status_code, 200)

    def test_document_file_print_view_no_permission(self):
        response = self._request_test_document_file_print_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_print_view_with_access(self):
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_print
        )

        response = self._request_test_document_file_print_view()
        self.assertEqual(response.status_code, 200)


class DocumentFileDownloadViewTestCase(
    DocumentFileViewTestMixin, GenericDocumentViewTestCase
):
    _test_event_object_name = 'test_document_file'

    def test_document_file_download_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_download_view()
        self.assertEqual(response.status_code, 404)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.file_latest.mimetype,
        )

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_download
        )

        self._clear_events()

        response = self._request_test_document_file_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_document.file_latest.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.file_latest.filename,
                mime_type=self.test_document.file_latest.mimetype
            )

        event = self._get_test_object_event()
        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_file)
        self.assertEqual(event.verb, event_document_file_downloaded.id)


class DocumentFileTransformationViewTestCase(
    LayerTestMixin, DocumentFileTransformationTestMixin,
    DocumentFileTransformationViewTestMixin, GenericDocumentViewTestCase
):
    test_document_filename = TEST_MULTI_PAGE_TIFF

    def test_document_file_transformations_clear_view_no_permission(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        response = self._request_test_document_file_transformations_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), transformation_count
        )

    def test_document_file_transformations_clear_view_with_access(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_transformation_delete
        )

        response = self._request_test_document_file_transformations_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), transformation_count - 1
        )

    def test_document_file_multiple_transformations_clear_view_no_permission(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        response = self._request_test_document_file_multiple_transformations_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), transformation_count
        )

    def test_document_file_multiple_transformations_clear_view_with_access(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_document_file_view
        )
        self.grant_access(
            obj=self.test_document_file,
            permission=permission_transformation_delete
        )

        response = self._request_test_document_file_multiple_transformations_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), transformation_count - 1,
        )

    def test_document_file_transformations_clone_view_no_permission(self):
        self._create_document_file_transformation()

        page_first_transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()
        page_last_transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.last()
        ).count()

        response = self._request_test_document_file_transformations_clone_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), page_first_transformation_count
        )
        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.last()
            ).count(), page_last_transformation_count
        )

    def test_document_file_transformations_clone_view_with_access(self):
        self._create_document_file_transformation()

        page_first_transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()
        page_last_transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.last()
        ).count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_transformation_edit
        )

        response = self._request_test_document_file_transformations_clone_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count(), page_first_transformation_count
        )
        self.assertEqual(
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.last()
            ).count(), page_last_transformation_count + 1
        )


class DocumentFileCachePurgeViewTestCase(
    CachePartitionViewTestMixin, ContentTypeTestCaseMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_cache_purge_no_permission(self):
        self.test_object = self.test_document_file
        self._inject_test_object_content_type()

        self.test_document_file.file_pages.first().generate_image()

        test_document_file_cache_partitions = self.test_document_file.get_cache_partitions()

        cache_partition_file_count = CachePartitionFile.objects.filter(
            partition__in=test_document_file_cache_partitions
        ).count()

        response = self._request_test_object_file_cache_partition_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            CachePartitionFile.objects.filter(
                partition__in=test_document_file_cache_partitions
            ).count(), cache_partition_file_count
        )

    def test_document_file_cache_purge_with_access(self):
        self.test_object = self.test_document_file
        self._inject_test_object_content_type()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_cache_partition_purge
        )

        self.test_document_file.file_pages.first().generate_image()

        test_document_file_cache_partitions = self.test_document_file.get_cache_partitions()

        cache_partition_file_count = CachePartitionFile.objects.filter(
            partition__in=test_document_file_cache_partitions
        ).count()

        response = self._request_test_object_file_cache_partition_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            CachePartitionFile.objects.filter(
                partition__in=test_document_file_cache_partitions
            ).count(), cache_partition_file_count
        )
