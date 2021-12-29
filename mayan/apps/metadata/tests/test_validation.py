from django.core.exceptions import ValidationError

from mayan.apps.common.serialization import yaml_dump
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import DocumentMetadata

from .literals import (
    TEST_DATE_INVALID, TEST_PARSER_DATE_VALID, TEST_VALID_DATE,
    TEST_VALIDATOR_PATH_DATE, TEST_VALIDATOR_PATH_REGULAR_EXPRESSION,
    TEST_VALIDATOR_REGULAR_EXPRESSION_PATTERN, TEST_VALIDATOR_VALUE_INVALID,
    TEST_VALIDATOR_VALUE_VALID
)
from .mixins import MetadataTypeTestMixin


class MetadataTypeValidationTestCase(
    DocumentTestMixin, MetadataTypeTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self._create_test_document_stub()

    def test_delete_document_metadata_with_validator(self):
        """
        GitLab issue #588 "Cannot delete metadata from document if
        validator or parser is set"
        """
        self._create_test_metadata_type(add_test_document_type=True)

        self.test_metadata_type.validation = TEST_VALIDATOR_PATH_DATE
        self.test_metadata_type.save()

        document_metadata = DocumentMetadata(
            document=self.test_document, metadata_type=self.test_metadata_type,
            value=TEST_PARSER_DATE_VALID
        )

        document_metadata.full_clean()
        document_metadata.save()

        # Must not raise an error
        document_metadata.delete()

    def test_validation_date(self):
        self._create_test_metadata_type(
            add_test_document_type=True, extra_kwargs={
                'validation': TEST_VALIDATOR_PATH_DATE
            }
        )

        document_metadata = DocumentMetadata(
            document=self.test_document, metadata_type=self.test_metadata_type,
            value=TEST_DATE_INVALID
        )

        with self.assertRaises(expected_exception=ValidationError):
            # Should return error
            document_metadata.full_clean()
            document_metadata.save()

        # Should not return error
        document_metadata.value = TEST_VALID_DATE
        document_metadata.full_clean()
        document_metadata.save()

        self.assertEqual(
            getattr(
                self.test_document.metadata_value_of,
                self.test_metadata_type.name
            ), TEST_VALID_DATE
        )

    def test_validator_regular_expression(self):
        self._create_test_metadata_type(
            add_test_document_type=True, extra_kwargs={
                'validation_arguments': yaml_dump(
                    data={
                        'pattern': TEST_VALIDATOR_REGULAR_EXPRESSION_PATTERN
                    }
                ),
                'validation': TEST_VALIDATOR_PATH_REGULAR_EXPRESSION
            }
        )

        with self.assertRaises(expected_exception=ValidationError):
            self.test_metadata_type.validate_value(
                document_type=None, value=TEST_VALIDATOR_VALUE_INVALID
            )

        self.test_metadata_type.validate_value(
            document_type=None, value=TEST_VALIDATOR_VALUE_VALID
        )
