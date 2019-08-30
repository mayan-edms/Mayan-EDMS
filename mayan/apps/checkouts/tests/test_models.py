from __future__ import unicode_literals

import time

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from ..exceptions import (
    DocumentAlreadyCheckedOut, DocumentNotCheckedOut,
    NewDocumentVersionNotAllowed
)
from ..models import DocumentCheckout, NewVersionBlock

from .mixins import DocumentCheckoutTestMixin


class DocumentCheckoutTestCase(
    DocumentCheckoutTestMixin, GenericDocumentTestCase
):
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

        with self.assertRaises(DocumentAlreadyCheckedOut):
            DocumentCheckout.objects.check_out_document(
                document=self.test_document,
                expiration_datetime=self._check_out_expiration_datetime,
                user=self._test_case_superuser,
                block_new_version=True
            )

    def test_document_check_in_without_check_out(self):
        with self.assertRaises(DocumentNotCheckedOut):
            self.test_document.check_in()

    def test_document_auto_check_in(self):
        self._check_out_test_document()

        # Ensure we wait from longer than the document check out expiration
        time.sleep(self._test_document_check_out_seconds + 0.1)

        DocumentCheckout.objects.check_in_expired_check_outs()

        self.assertFalse(self.test_document.is_checked_out())


class NewVersionBlockTestCase(
    DocumentCheckoutTestMixin, DocumentTestMixin, BaseTestCase
):
    def test_blocking(self):
        NewVersionBlock.objects.block(document=self.test_document)

        self.assertEqual(NewVersionBlock.objects.count(), 1)
        self.assertEqual(
            NewVersionBlock.objects.first().document, self.test_document
        )

    def test_blocking_new_versions(self):
        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.documents.models')

        NewVersionBlock.objects.block(document=self.test_document)

        with self.assertRaises(NewDocumentVersionNotAllowed):
            with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
                self.test_document.new_version(file_object=file_object)

    def test_unblocking(self):
        NewVersionBlock.objects.create(document=self.test_document)

        NewVersionBlock.objects.unblock(document=self.test_document)

        self.assertEqual(NewVersionBlock.objects.count(), 0)

    def test_is_blocked(self):
        NewVersionBlock.objects.create(document=self.test_document)

        self.assertTrue(
            NewVersionBlock.objects.is_blocked(document=self.test_document)
        )

        NewVersionBlock.objects.all().delete()

        self.assertFalse(
            NewVersionBlock.objects.is_blocked(document=self.test_document)
        )

    def test_version_creation_blocking(self):
        # Silence unrelated logging
        self._silence_logger(name='mayan.apps.documents.models')

        self._create_test_case_superuser()

        self._check_out_test_document()

        with self.assertRaises(NewDocumentVersionNotAllowed):
            with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
                self.test_document.new_version(file_object=file_object)
