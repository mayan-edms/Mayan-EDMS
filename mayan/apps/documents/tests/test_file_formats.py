from .base import GenericDocumentTestCase
from .literals import TEST_FILE_MULTI_PAGE_TIFF_FILENAME, TEST_FILE_OFFICE


class OfficeTextDocumentTestCase(GenericDocumentTestCase):
    _test_document_filename = TEST_FILE_OFFICE

    def test_document_creation(self):
        self.assertEqual(
            self._test_document.file_latest.mimetype, 'application/msword'
        )
        self.assertEqual(
            self._test_document.file_latest.encoding, 'binary'
        )
        self.assertEqual(
            self._test_document.file_latest.checksum,
            '03a7e9071d2c6ae05a6588acd7dff1d890fac2772cf61abd470c9ffa6ef71f03'
        )
        self.assertEqual(self._test_document.pages.count(), 2)


class MultiPageTiffTestCase(GenericDocumentTestCase):
    _test_document_filename = TEST_FILE_MULTI_PAGE_TIFF_FILENAME

    def test_document_creation(self):
        self.assertEqual(self._test_document.file_latest.mimetype, 'image/tiff')
        self.assertEqual(self._test_document.file_latest.encoding, 'binary')
        self.assertEqual(
            self._test_document.file_latest.checksum,
            '40adaa9d658b65c70a7f002dfe084a8354bb77c0dfbf1993e31fb024a285fb1d'
        )
        self.assertEqual(self._test_document.pages.count(), 2)
