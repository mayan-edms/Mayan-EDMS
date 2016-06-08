from __future__ import unicode_literals

from django.core.files.base import File
from django.core.exceptions import ValidationError
from django.test import override_settings

from documents.models import DocumentType
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
from organizations.tests import OrganizationTestCase

from ..models import MetadataType, DocumentMetadata

from .literals import (
    TEST_DEFAULT_VALUE, TEST_LOOKUP_TEMPLATE, TEST_INCORRECT_LOOKUP_VALUE,
    TEST_CORRECT_LOOKUP_VALUE, TEST_DATE_VALIDATOR, TEST_DATE_PARSER,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_LABEL, TEST_INVALID_DATE,
    TEST_VALID_DATE, TEST_PARSED_VALID_DATE
)


@override_settings(OCR_AUTO_OCR=False)
class MetadataTestCase(OrganizationTestCase):
    def setUp(self):
        super(MetadataTestCase, self).setUp()
        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.metadata_type = MetadataType.on_organization.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )

        self.document_type.metadata.create(metadata_type=self.metadata_type)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()
        super(MetadataTestCase, self).tearDown()

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

        self.assertEqual(
            self.document.metadata_value_of.test, TEST_DEFAULT_VALUE
        )

    def test_lookup_with_incorrect_value(self):
        self.metadata_type.lookup = TEST_LOOKUP_TEMPLATE
        self.metadata_type.save()

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type,
            value=TEST_INCORRECT_LOOKUP_VALUE
        )

        with self.assertRaises(ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

    def test_lookup_with_correct_value(self):
        self.metadata_type.lookup = TEST_LOOKUP_TEMPLATE
        self.metadata_type.save()

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type,
            value=TEST_CORRECT_LOOKUP_VALUE
        )

        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(
            self.document.metadata_value_of.test, TEST_CORRECT_LOOKUP_VALUE
        )

    def test_empty_optional_lookup(self):
        """
        Checks for GitLab issue #250
        Empty optional lookup metadata trigger validation error
        """

        self.metadata_type.lookup = TEST_LOOKUP_TEMPLATE
        self.metadata_type.save()

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type
        )

        document_metadata.full_clean()
        document_metadata.save()

    def test_validation(self):
        self.metadata_type.validation = TEST_DATE_VALIDATOR

        document_metadata = DocumentMetadata(
            document=self.document, metadata_type=self.metadata_type,
            value=TEST_INVALID_DATE
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
            document=self.document, metadata_type=self.metadata_type,
            value=TEST_INVALID_DATE
        )

        with self.assertRaises(ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

        # Should not return error
        document_metadata.value = TEST_VALID_DATE
        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(
            self.document.metadata_value_of.test, TEST_PARSED_VALID_DATE
        )

    def test_required_metadata(self):
        self.document_type.metadata.all().delete()

        self.assertFalse(
            self.metadata_type.get_required_for(self.document_type)
        )

        self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=False
        )

        self.assertFalse(
            self.metadata_type.get_required_for(self.document_type)
        )

        self.document_type.metadata.all().delete()

        self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=True
        )

        self.assertTrue(
            self.metadata_type.get_required_for(self.document_type)
        )
