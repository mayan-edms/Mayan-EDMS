from django.utils.encoding import force_text

from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.permissions import permission_transformation_delete
from mayan.apps.converter.tests.mixins import LayerTestMixin

from ..permissions import (
    permission_document_file_download, permission_document_file_delete,
    permission_document_file_view, permission_document_tools,
)

from .base import GenericDocumentViewTestCase
from .literals import TEST_SMALL_DOCUMENT_FILENAME, TEST_VERSION_COMMENT
from .mixins.document_file_mixins import (
    DocumentFileTestMixin, DocumentFileViewTestMixin
)


class DocumentFilePreviewViewTestCase(
    DocumentFileTestMixin, DocumentFilePreviewViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_list_no_permission(self):
        self._upload_new_file()

        response = self._request_document_file_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_file_list_with_access(self):
        self._upload_new_file()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        response = self._request_document_file_list_view()
        self.assertContains(
            response=response, status_code=200, text=TEST_VERSION_COMMENT
        )

    def test_document_file_delete_no_permission(self):
        first_file = self.test_document.latest_file
        self._upload_new_file()

        response = self._request_document_file_delete_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.files.count(), 2)

    def test_document_file_delete_with_access(self):
        first_file = self.test_document.latest_file
        self._upload_new_file()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_delete
        )

        response = self._request_document_file_delete_view(
            document_file=first_file
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.files.count(), 1)

    def test_document_update_page_count_view_no_permission(self):
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        response = self._request_test_document_update_page_count_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.pages.count(), 0)

    def test_document_update_page_count_view_with_permission(self):
        page_count = self.test_document.pages.count()
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        self.grant_access(
            obj=self.test_document, permission=permission_document_tools
        )

        response = self._request_test_document_update_page_count_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.pages.count(), page_count)

    def test_document_multiple_update_page_count_view_no_permission(self):
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        response = self._request_test_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_document.pages.count(), 0)

    def test_document_multiple_update_page_count_view_with_permission(self):
        page_count = self.test_document.pages.count()
        self.test_document.pages.all().delete()
        self.assertEqual(self.test_document.pages.count(), 0)

        self.grant_access(
            obj=self.test_document, permission=permission_document_tools
        )

        response = self._request_test_document_multiple_update_page_count_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_document.pages.count(), page_count)


class DocumentFileDownloadViewTestCase(
    DocumentFileTestMixin, DocumentFilePreviewViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_download_view_no_permission(self):
        response = self._request_document_file_download()
        self.assertEqual(response.status_code, 404)

    def test_document_file_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_file.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_document_file_download()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(self.test_document.latest_file),
                mime_type=self.test_document.latest_file.mimetype
            )

    def test_document_file_download_preserve_extension_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.latest_file.mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_document_file_download(
            data={'preserve_extension': True}
        )
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.latest_file.get_rendered_string(
                    preserve_extension=True
                ), mime_type=self.test_document.latest_file.mimetype
            )

    def test_document_download_form_get_view_no_permission(self):
        response = self._request_test_document_download_form_get_view()
        self.assertEqual(response.status_code, 404)

    def test_document_download_form_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_test_document_download_form_get_view()
        self.assertContains(
            response=response, status_code=200, text=self.test_document.label
        )

    def test_document_download_form_post_view_no_permission(self):
        response = self._request_test_document_download_form_post_view()
        self.assertEqual(response.status_code, 404)

    def test_document_download_form_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )
        response = self._request_test_document_download_form_post_view()
        self.assertEqual(response.status_code, 302)

    def test_document_download_view_no_permission(self):
        response = self._request_test_document_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.file_mimetype,
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_test_document_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.test_document.file_mimetype
            )

    def test_document_multiple_download_view_no_permission(self):
        response = self._request_test_document_multiple_download_view()
        self.assertEqual(response.status_code, 404)

    def test_document_multiple_download_view_with_permission(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = (
            self.test_document.file_mimetype,
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_download
        )

        response = self._request_test_document_multiple_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=TEST_SMALL_DOCUMENT_FILENAME,
                mime_type=self.test_document.file_mimetype
            )


class DocumentFileTransformationViewTestCase(
    LayerTestMixin, DocumentFileTestMixin, DocumentFilePreviewViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_file_clear_transformations_view_no_permission(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file, permission=permission_document_file_view
        )

        response = self._request_test_document_file_clear_transformations_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            transformation_count,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count()
        )

    def test_document_file_clear_transformations_view_with_access(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file,
            permission=permission_transformation_delete
        )
        self.grant_access(
            obj=self.test_document_file, permission=permission_document_file_view
        )

        response = self._request_test_document_file_clear_transformations_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            transformation_count - 1,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count()
        )

    def test_document_file_multiple_clear_transformations_view_no_permission(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file, permission=permission_document_file_view
        )

        response = self._request_test_document_file_multiple_clear_transformations()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            transformation_count,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count()
        )

    def test_document_file_multiple_clear_transformations_view_with_access(self):
        self._create_document_file_transformation()

        transformation_count = layer_saved_transformations.get_transformations_for(
            obj=self.test_document_file.pages.first()
        ).count()

        self.grant_access(
            obj=self.test_document_file, permission=permission_document_file_view
        )
        self.grant_access(
            obj=self.test_document_file, permission=permission_transformation_delete
        )

        response = self._request_test_document_file_multiple_clear_transformations()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            transformation_count - 1,
            layer_saved_transformations.get_transformations_for(
                obj=self.test_document_file.pages.first()
            ).count()
        )
