from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.documents.tests import (
    GenericDocumentViewTestCase, TEST_HYBRID_DOCUMENT
)

from ..permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)
from ..utils import get_document_content

from .literals import TEST_DOCUMENT_CONTENT


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentContentViewsTestCase(GenericDocumentViewTestCase):
    _skip_file_descriptor_test = True

    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def _request_document_content_view(self):
        return self.get(
            'document_parsing:document_content', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_content_view_no_permissions(self):
        response = self._request_document_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_content_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_content_view
        )

        response = self._request_document_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def _request_document_page_content_view(self):
        return self.get(
            viewname='document_parsing:document_page_content', kwargs={
                'pk': self.test_document.pages.first().pk,
            }
        )

    def test_document_page_content_view_no_permissions(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, 404)

    def test_document_page_content_view_with_access(self):
        self.grant_access(
            permission=permission_content_view, obj=self.test_document
        )

        response = self._request_document_page_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_CONTENT, status_code=200
        )

    def _request_document_content_download_view(self):
        return self.get(
            viewname='document_parsing:document_content_download',
            kwargs={'pk': self.test_document.pk}
        )

    def test_document_parsing_download_view_no_permission(self):
        response = self._request_document_content_download_view()
        self.assertEqual(response.status_code, 403)

    def test_download_view_with_access(self):
        self.expected_content_type = 'application/octet-stream; charset=utf-8'
        self.grant_access(
            permission=permission_content_view, obj=self.test_document
        )

        response = self._request_document_content_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=(
                ''.join(get_document_content(document=self.test_document))
            ),
        )

    def _request_test_document_type_parsing_settings(self):
        return self.get(
            viewname='document_parsing:document_type_parsing_settings',
            kwargs={'pk': self.test_document.document_type.pk}
        )

    def test_document_type_parsing_settings_view_no_permission(self):
        response = self._request_test_document_type_parsing_settings()
        self.assertEqual(response.status_code, 404)

    def test_document_type_parsing_settings_view_with_access(self):
        self.grant_access(
            permission=permission_document_type_parsing_setup,
            obj=self.test_document.document_type
        )

        response = self._request_test_document_type_parsing_settings()
        self.assertEqual(response.status_code, 200)


class DocumentContentToolsViewsTestCase(GenericDocumentViewTestCase):
    _skip_file_descriptor_test = True

    # Ensure we use a PDF file
    test_document_filename = TEST_HYBRID_DOCUMENT

    def _request_document_parsing_tool_view(self):
        return self.post(
            viewname='document_parsing:document_type_submit', data={
                'document_type': self.test_document_type.pk
            }
        )

    def _get_document_content(self):
        return ''.join(list(get_document_content(document=self.test_document)))

    def test_document_parsing_tool_view_no_permission(self):

        response = self._request_document_parsing_tool_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_document_type.label
        )

        self.assertNotEqual(
            self._get_document_content(), TEST_DOCUMENT_CONTENT
        )

    def test_document_parsing_tool_view_with_permission(self):
        self.grant_permission(permission=permission_parse_document)

        response = self._request_document_parsing_tool_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._get_document_content(), TEST_DOCUMENT_CONTENT
        )
