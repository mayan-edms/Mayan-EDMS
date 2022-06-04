from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import SignatureCaptureTestMixin


class SignatureCaptureModelTestCase(
    SignatureCaptureTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_method_get_absolute_url(self):
        self._create_test_signature_capture()

        self.assertTrue(self._test_signature_capture.get_absolute_url())
