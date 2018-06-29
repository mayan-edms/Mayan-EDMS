from __future__ import unicode_literals

from django.test import override_settings

from documents.tests import (
    GenericDocumentViewTestCase, TEST_DOCUMENT_FILENAME,
    TEST_DOCUMENT_PATH
)

from ..permissions import permission_content_view
from ..utils import get_document_content


@override_settings(DOCUMENT_PARSING_AUTO_PARSING=True)
class DocumentContentViewsTestCase(GenericDocumentViewTestCase):
    _skip_file_descriptor_test = True

    # Ensure we use a PDF file
    test_document_filename = TEST_DOCUMENT_FILENAME
    test_document_path = TEST_DOCUMENT_PATH

    def setUp(self):
        super(DocumentContentViewsTestCase, self).setUp()
        self.login_user()

    def _document_content_view(self):
        return self.get(
            'document_parsing:document_content', args=(self.document.pk,)
        )

    def test_document_content_view_no_permissions(self):
        response = self._document_content_view()

        self.assertEqual(response.status_code, 403)

    def test_document_content_view_with_permission(self):
        self.grant_permission(permission=permission_content_view)
        response = self._document_content_view()

        self.assertContains(
            response, 'Mayan EDMS Documentation', status_code=200
        )

    def test_document_parsing_download_view_no_permission(self):
        response = self.get(
            'document_parsing:document_content_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_download_view_with_permission(self):
        self.expected_content_type = 'application/octet-stream; charset=utf-8'

        self.grant_permission(permission=permission_content_view)
        response = self.get(
            'document_parsing:document_content_download', args=(self.document.pk,)
        )

        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response, content=(
                ''.join(get_document_content(document=self.document))
            ),
        )
