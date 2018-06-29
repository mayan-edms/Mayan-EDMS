from __future__ import unicode_literals

from documents.tests import GenericDocumentViewTestCase

from ..permissions import permission_ocr_content_view, permission_ocr_document
from ..utils import get_document_ocr_content


class OCRViewsTestCase(GenericDocumentViewTestCase):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    def setUp(self):
        super(OCRViewsTestCase, self).setUp()
        self.login_user()

    def _request_document_content_view(self):
        return self.get(
            'ocr:document_content', args=(self.document.pk,)
        )

    def test_document_content_view_no_permissions(self):
        self.document.submit_for_ocr()
        response = self._request_document_content_view()

        self.assertEqual(response.status_code, 403)

    def test_document_content_view_with_access(self):
        self.document.submit_for_ocr()
        self.grant_access(
            permission=permission_ocr_content_view, obj=self.document
        )

        response = self._request_document_content_view()

        self.assertContains(
            response, 'Mayan EDMS Documentation', status_code=200
        )

    def _request_document_submit_view(self):
        return self.post(
            'ocr:document_submit', args=(self.document.pk,)
        )

    def test_document_submit_view_no_permission(self):
        self._request_document_submit_view()
        self.assertEqual(
            ''.join(self.document.latest_version.ocr_content()), ''
        )

    def test_document_submit_view_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.document
        )
        self._request_document_submit_view()
        self.assertTrue(
            'Mayan EDMS Documentation' in ''.join(
                self.document.latest_version.ocr_content()
            )
        )

    def _request_multiple_document_submit_view(self):
        return self.post(
            'ocr:document_submit_multiple',
            data={
                'id_list': self.document.pk,
            }
        )

    def test_multiple_document_submit_view_no_permission(self):
        self._request_multiple_document_submit_view()
        self.assertEqual(
            ''.join(self.document.latest_version.ocr_content()), ''
        )

    def test_multiple_document_submit_view_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.document
        )
        self._request_multiple_document_submit_view()
        self.assertTrue(
            'Mayan EDMS Documentation' in ''.join(
                self.document.latest_version.ocr_content()
            )
        )

    def _request_document_ocr_download_view(self):
        return self.get(
            'ocr:document_ocr_download', args=(self.document.pk,)
        )

    def test_document_ocr_download_view_no_permission(self):
        self.document.submit_for_ocr()
        response = self._request_document_ocr_download_view()
        self.assertEqual(response.status_code, 403)

    def test_document_ocr_download_view_with_permission(self):
        self.document.submit_for_ocr()
        self.expected_content_type = 'application/octet-stream; charset=utf-8'

        self.grant_permission(permission=permission_ocr_content_view)
        response = self._request_document_ocr_download_view()

        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response, content=(
                ''.join(get_document_ocr_content(document=self.document))
            ),
        )
