from __future__ import unicode_literals

from common.tests import BaseTestCase

from ..models import MetadataType, DocumentMetadata

from .literals import (
    TEST_DEFAULT_VALUE, TEST_LOOKUP_TEMPLATE, TEST_INCORRECT_LOOKUP_VALUE,
    TEST_CORRECT_LOOKUP_VALUE, TEST_DATE_VALIDATOR, TEST_DATE_PARSER,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_LABEL, TEST_INVALID_DATE,
    TEST_VALID_DATE, TEST_PARSED_VALID_DATE
)


class MetadataTypeMixin(object):
    def setUp(self):
        super(MetadataTypeMixin, self).setUp()
        self.metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )
