from django.core.exceptions import ValidationError

from mayan.apps.common.serialization import yaml_dump
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import DocumentMetadata

from .literals import (
    TEST_DATE_INVALID, TEST_PARSER_PATH_DATE, TEST_PARSER_DATE_VALID,
    TEST_PARSER_REGULAR_EXPRESSION, TEST_PARSER_REGULAR_EXPRESSION_PATTERN,
    TEST_PARSER_REGULAR_EXPRESSION_REPLACEMENT_TEXT, TEST_VALID_DATE
)
from .mixins import MetadataTypeTestMixin


class MetadataTypeParsingTestCase(
    DocumentTestMixin, MetadataTypeTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_parsing_date(self):
        self._create_test_metadata_type(
            add_test_document_type=True, extra_kwargs={
                'parser': TEST_PARSER_PATH_DATE
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
            ), TEST_PARSER_DATE_VALID
        )

    def test_parser_regular_expression(self):
        self._create_test_metadata_type(
            add_test_document_type=True, extra_kwargs={
                'parser': TEST_PARSER_REGULAR_EXPRESSION
            }
        )

        self._create_test_metadata_type(
            add_test_document_type=True, extra_kwargs={
                'parser': TEST_PARSER_REGULAR_EXPRESSION,
                'parser_arguments': yaml_dump(
                    data={
                        'pattern': TEST_PARSER_REGULAR_EXPRESSION_PATTERN,
                        'replacement': TEST_PARSER_REGULAR_EXPRESSION_REPLACEMENT_TEXT
                    }
                )
            }
        )

        document_metadata = DocumentMetadata(
            document=self.test_document, metadata_type=self.test_metadata_type,
            value=TEST_PARSER_REGULAR_EXPRESSION_PATTERN
        )

        document_metadata.full_clean()
        self.assertEqual(
            document_metadata.value,
            TEST_PARSER_REGULAR_EXPRESSION_REPLACEMENT_TEXT
        )
