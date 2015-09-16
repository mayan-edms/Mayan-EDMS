from __future__ import unicode_literals

from django.core.files.base import File
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from documents.models import DocumentType
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE

from ..models import MetadataType, DocumentMetadata

TEST_DEFAULT_VALUE = 'test'
TEST_LOOKUP_TEMPLATE = '1,2,3'
TEST_INCORRECT_LOOKUP_VALUE = '0'
TEST_CORRECT_LOOKUP_VALUE = '1'
TEST_DATE_VALIDATOR = 'metadata.validators.DateValidator'
TEST_DATE_PARSER = 'metadata.parsers.DateParser'
TEST_INVALID_DATE = '___________'
TEST_VALID_DATE = '2001-1-1'
TEST_PARSED_VALID_DATE = '2001-01-01'


@override_settings(OCR_AUTO_OCR=False)
class MetadataTestCase(TestCase):
    def setUp(self):
        self.metadata_type = MetadataType.objects.create(
            name='test', label='test'
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.document_type.metadata.create(metadata_type=self.metadata_type)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()
        self.metadata_type.delete()

    def test_no_default(self):
        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type
        )

        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(self.document.metadata_value_of.test, None)

    def test_default(self):
        self.metadata_type.default = TEST_DEFAULT_VALUE
        self.metadata_type.save()

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type
        )

        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(self.document.metadata_value_of.test, TEST_DEFAULT_VALUE)

    def test_lookup(self):
        self.metadata_type.lookup = TEST_LOOKUP_TEMPLATE

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type, value=TEST_INCORRECT_LOOKUP_VALUE
        )

        with self.assertRaises(ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

        # Should not return error
        document_metadata.value = TEST_CORRECT_LOOKUP_VALUE
        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(self.document.metadata_value_of.test, TEST_CORRECT_LOOKUP_VALUE)

    def test_validation(self):
        self.metadata_type.validation = TEST_DATE_VALIDATOR

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type, value=TEST_INVALID_DATE
        )

        with self.assertRaises(ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

        # Should not return error
        document_metadata.value = TEST_VALID_DATE
        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(self.document.metadata_value_of.test, TEST_VALID_DATE)

    def test_parsing(self):
        self.metadata_type.parser = TEST_DATE_PARSER

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type, value=TEST_INVALID_DATE
        )

        with self.assertRaises(ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

        # Should not return error
        document_metadata.value = TEST_VALID_DATE
        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(self.document.metadata_value_of.test, TEST_PARSED_VALID_DATE)
