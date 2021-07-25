from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..exceptions import (
    DocumentAlreadyCheckedOut, DocumentNotCheckedOut,
    NewDocumentFileNotAllowed
)
from ..models import DocumentCheckout

from .mixins import DocumentCheckoutTestMixin


class DocumentCheckoutTestCase(
    DocumentCheckoutTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_document_check_out(self):
        self._check_out_test_document()

        self.assertTrue(
            DocumentCheckout.objects.is_checked_out(
                document=self.test_document
            )
        )

    def test_document_check_in(self):
        self._check_out_test_document()

        self.test_document.check_in()

        self.assertFalse(self.test_document.is_checked_out())
        self.assertFalse(
            DocumentCheckout.objects.is_checked_out(
                document=self.test_document
            )
        )

    def test_document_double_check_out(self):
        self._create_test_case_superuser()
        self._check_out_test_document()

        with self.assertRaises(expected_exception=DocumentAlreadyCheckedOut):
            DocumentCheckout.objects.check_out_document(
                document=self.test_document,
                expiration_datetime=self._check_out_expiration_datetime,
                user=self._test_case_superuser,
                block_new_file=True
            )

    def test_document_check_in_without_check_out(self):
        with self.assertRaises(expected_exception=DocumentNotCheckedOut):
            self.test_document.check_in()

    def test_document_auto_check_in(self):
        self._check_out_test_document()

        # Ensure we wait from longer than the document check out expiration
        self._test_delay(seconds=self._test_document_check_out_seconds + 0.1)

        DocumentCheckout.objects.check_in_expired_check_outs()

        self.assertFalse(self.test_document.is_checked_out())

    def test_method_get_absolute_url(self):
        self._check_out_test_document()

        self.assertTrue(self.test_check_out.get_absolute_url())

    def test_blocking_new_files(self):
        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.documents.models')
        self._check_out_test_document()

        with self.assertRaises(expected_exception=NewDocumentFileNotAllowed):
            with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
                self.test_document.file_new(file_object=file_object)

    def test_file_creation_blocking(self):
        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.documents.models')

        self._create_test_case_superuser()

        self._check_out_test_document()

        with self.assertRaises(expected_exception=NewDocumentFileNotAllowed):
            with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
                self.test_document.file_new(file_object=file_object)
