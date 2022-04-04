from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_file_new
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..links import link_document_create_multiple, link_document_file_upload

from .mixins.base_mixins import SourceTestMixin


class SourcesNewDocumentLinkTestCase(
    SourceTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def _get_document_create_link(self):
        self.add_test_view()
        context = self.get_test_view()
        context['user'] = self._test_case_user
        return link_document_create_multiple.resolve(context=context)

    def test_document_create_link_no_permission(self):
        resolved_link = self._get_document_create_link()
        self.assertEqual(resolved_link, None)

    def test_document_create_link_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )

        resolved_link = self._get_document_create_link()
        self.assertEqual(resolved_link, None)

    def test_document_create_link_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        resolved_link = self._get_document_create_link()
        self.assertEqual(resolved_link, None)

    def test_document_create_link_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        resolved_link = self._get_document_create_link()
        self.assertNotEqual(resolved_link, None)


class SourcesNewDocumentFileLinkTestCase(
    SourceTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def _get_document_file_upload_link(self):
        self.add_test_view(test_object=self.test_document)
        context = self.get_test_view()
        context['user'] = self._test_case_user
        return link_document_file_upload.resolve(context=context)

    def test_document_file_upload_link_no_permission(self):
        resolved_link = self._get_document_file_upload_link()
        self.assertEqual(resolved_link, None)

    def test_document_file_upload_link_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_new
        )

        resolved_link = self._get_document_file_upload_link()
        self.assertEqual(resolved_link, None)

    def test_document_file_upload_link_with_source_access(self):
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )

        resolved_link = self._get_document_file_upload_link()
        self.assertEqual(resolved_link, None)

    def test_document_file_upload_link_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_new
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_file_new
        )

        resolved_link = self._get_document_file_upload_link()
        self.assertNotEqual(resolved_link, None)
