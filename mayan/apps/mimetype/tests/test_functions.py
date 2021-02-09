import resource
import unittest

from django.test import override_settings, tag

from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.documents.tests.literals import TEST_PDF_DOCUMENT_FILENAME
from mayan.apps.testing.literals import EXCLUDE_TEST_TAG
from mayan.apps.testing.tests.base import BaseTestCase

from .literals import MAXIMUM_HEAP_MEMORY


@unittest.skip('This test should be used only in development.')
@tag('memory', EXCLUDE_TEST_TAG)
class MIMETypeTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_test_document = False
    test_document_filename = TEST_PDF_DOCUMENT_FILENAME

    def setUp(self):
        super().setUp()
        resource.setrlimit(resource.RLIMIT_DATA, (MAXIMUM_HEAP_MEMORY, -1))

    def test_little_memory_full_file(self):
        with self.assertRaises(expected_exception=Exception):
            self._upload_test_document()

        self.assertEqual(Document.objects.count(), 0)

    @override_settings(MIMETYPE_FILE_READ_SIZE=1024)
    def test_little_memory_partial_file(self):
        self._upload_test_document()

        self.assertEqual(Document.objects.count(), 1)
