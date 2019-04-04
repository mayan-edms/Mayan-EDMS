from __future__ import unicode_literals

import resource

from django.test import override_settings, tag

from common.tests import BaseTestCase
from common.tests.literals import EXCLUDE_TEST_TAG
from documents.models import Document
from documents.tests import DocumentTestMixin, TEST_DOCUMENT_FILENAME

# This constant may need tweaking as document upload code path changes.
# The value is targeted at making the document upload process fail exactly
# during the MIME type detection phase. Different architectures may need
# different values.
MAXIMUM_HEAP_MEMORY = 140000000


@override_settings(OCR_AUTO_OCR=False)
@override_settings(DOCUMENT_PARSING_AUTO_PARSING=False)
@tag('memory', EXCLUDE_TEST_TAG)
class MIMETypeTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False
    test_document_filename = TEST_DOCUMENT_FILENAME

    def setUp(self):
        super(MIMETypeTestCase, self).setUp()
        resource.setrlimit(resource.RLIMIT_DATA, (MAXIMUM_HEAP_MEMORY, -1))

    def test_little_memory_full_file(self):
        with self.assertRaises(Exception):
            self.upload_document()

        self.assertEqual(Document.objects.count(), 0)

    @override_settings(MIMETYPE_FILE_READ_SIZE=1024)
    def test_little_memory_partial_file(self):
        self.upload_document()

        self.assertEqual(Document.objects.count(), 1)
