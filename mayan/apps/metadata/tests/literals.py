# -*- coding: utf-8 -*-

DOCUMENT_METADATA_ADD_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataAddAction'
DOCUMENT_METADATA_EDIT_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataEditAction'
DOCUMENT_METADATA_REMOVE_ACTION_CLASS_PATH = 'mayan.apps.metadata.workflow_actions.DocumentMetadataRemoveAction'

TEST_DATE_INVALID = '___________'
TEST_DEFAULT_VALUE = 'test'

TEST_LOOKUP_TEMPLATE = '1,2,3'
TEST_LOOKUP_VALUE_CORRECT = '1'
TEST_LOOKUP_VALUE_INCORRECT = '0'

TEST_METADATA_INDEX_NODE_TEMPLATE = '{{ document.metadata.first.metadata_type.label }}-{{ document.metadata.first.value }}'

TEST_METADATA_TYPE_DEFAULT_VALUE = 'default value'
TEST_METADATA_TYPE_LABEL = 'test metadata type label'
TEST_METADATA_TYPE_LABEL_EDITED = 'test metadata type label edited'
TEST_METADATA_TYPE_NAME = 'test_metadata_type_name'
TEST_METADATA_TYPE_NAME_EDITED = 'test_metadata_type_name_edited'
TEST_METADATA_VALUE = 'test value'
TEST_METADATA_VALUE_EDITED = 'test value edited'
TEST_METADATA_VALUE_UNICODE = 'español'
TEST_METADATA_VALUE_WITH_AMPERSAND = 'first value & second value'

TEST_PARSER_DATE_VALID = '2001-01-01'
TEST_PARSER_PATH_DATE = 'mayan.apps.metadata.metadata_parsers.DateParser'

TEST_PARSER_REGULAR_EXPRESSION = 'mayan.apps.metadata.metadata_parsers.RegularExpressionParser'
TEST_PARSER_REGULAR_EXPRESSION_PATTERN = 'abc'
TEST_PARSER_REGULAR_EXPRESSION_REPLACEMENT_TEXT = 'replaced_text'

TEST_VALID_DATE = '2001-1-1'
TEST_VALIDATOR_PATH_DATE = 'mayan.apps.metadata.metadata_validators.DateValidator'
TEST_VALIDATOR_PATH_REGULAR_EXPRESSION = 'mayan.apps.metadata.metadata_validators.RegularExpressionValidator'
TEST_VALIDATOR_REGULAR_EXPRESSION_PATTERN = '^[A-Za-z]*$'
TEST_VALIDATOR_VALUE_INVALID = '1234'
TEST_VALIDATOR_VALUE_VALID = 'abcd'
