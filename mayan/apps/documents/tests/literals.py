# -*- coding: utf-8 -*-

import os

from django.conf import settings

from mayan.apps.common.literals import TIME_DELTA_UNIT_DAYS
from mayan.apps.converter.transformations import TransformationRotate

from ..literals import (
    DEFAULT_DOCUMENTS_RECENTLY_ACCESSED_COUNT,
    DEFAULT_DOCUMENTS_RECENTLY_CREATED_COUNT
)

DEFAULT_DOCUMENT_STUB_LABEL = 'document_stub'

# Filenames
TEST_FILE_COMPRESSED_FILENAME = 'compressed_documents.zip'
TEST_FILE_GERMAN_FILENAME = 'deu_website.png'
TEST_FILE_HYBRID_PDF_FILENAME = 'hybrid_text_and_image.pdf'
TEST_FILE_MULTI_PAGE_TIFF_FILENAME = 'multi_page.tiff'
TEST_FILE_NON_ASCII_COMPRESSED_FILENAME = 'I18N_title_áéíóúüñÑ.png.zip'
TEST_FILE_NON_ASCII_FILENAME = 'I18N_title_áéíóúüñÑ.png'
TEST_FILE_OFFICE = 'simple_2_page_document.doc'
TEST_FILE_PDF_FILENAME = 'mayan_11_1.pdf'
TEST_FILE_SMALL_FILENAME = 'title_page.png'
TEST_FILE_TEXT_FILENAME = 'sample_file_text.txt'

TEST_FILE_HYBRID_PDF_CONTENT = 'Sample text'
TEST_FILE_OFFICE_CONTENT = 'First page'
TEST_FILE_TEXT_CONTENT = 'Sample_text_file_content'

TEST_DOCUMENT_DESCRIPTION = 'test description'
TEST_DOCUMENT_DESCRIPTION_EDITED = 'test document description edited'
TEST_DOCUMENT_FILE_COMMENT = 'test document file comment'
TEST_DOCUMENT_FILE_COMMENT_EDITED = 'test document file comment edited'
TEST_DOCUMENT_FILE_FILENAME_EDITED = 'test document file filename edited'
TEST_DOCUMENT_LABEL_EDITED = 'test document label edited'
TEST_DOCUMENT_SMALL_CHECKSUM = 'efa10e6cc21f83078aaa94d5cbe51de67b51af706143b\
afc7fd6d4c02124879a'
TEST_DOCUMENT_SMALL_MIMETYPE = 'image/png'
TEST_DOCUMENT_SMALL_SIZE = 17436
TEST_DOCUMENT_TYPE_DELETE_PERIOD = 30
TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT = TIME_DELTA_UNIT_DAYS
TEST_DOCUMENT_TYPE_LABEL = 'test_document_type'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2'
TEST_DOCUMENT_TYPE_LABEL_EDITED = 'test document type label edited'
TEST_DOCUMENT_TYPE_QUICK_LABEL = 'test quick label'
TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED = 'test quick label edited'
TEST_DOCUMENT_VERSION_COMMENT = 'test document version comment'
TEST_DOCUMENT_VERSION_COMMENT_EDITED = 'test document version comment edited'
TEST_DUPLICATED_DOCUMENT_LABEL = 'test duplicated document label'

TEST_TRANSFORMATION_CLASS = TransformationRotate
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'

# File paths
TEST_FILE_COMPRESSED_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_COMPRESSED_FILENAME
)
TEST_FILE_GERMAN_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_GERMAN_FILENAME
)
TEST_FILE_HYBRID_PDF_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_HYBRID_PDF_FILENAME
)
TEST_FILE_MULTI_PAGE_TIFF_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_MULTI_PAGE_TIFF_FILENAME
)
TEST_FILE_NON_ASCII_COMPRESSED_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_NON_ASCII_COMPRESSED_FILENAME
)
TEST_FILE_NON_ASCII_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_NON_ASCII_FILENAME
)
TEST_FILE_OFFICE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_OFFICE
)
TEST_FILE_PDF_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_PDF_FILENAME
)
TEST_FILE_SMALL_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_SMALL_FILENAME
)
TEST_FILE_TEXT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_FILE_TEXT_FILENAME
)

# Test settings migrations

TEST_DOCUMENTS_CACHE_STORAGE_BACKEND = 'test.backend'
TEST_DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS = {'location': 'test value'}
TEST_DOCUMENTS_STORAGE_BACKEND = 'test.backend'
TEST_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS = {'location': 'test value'}
TEST_DOCUMENTS_RECENTLY_CREATED_COUNT = DEFAULT_DOCUMENTS_RECENTLY_CREATED_COUNT * 2
TEST_DOCUMENTS_RECENTLY_ACCESSED_COUNT = DEFAULT_DOCUMENTS_RECENTLY_ACCESSED_COUNT * 2

# Workflows

TEST_DOCUMENT_TYPE_CHANGE_ACTION_DOTTED_PATH = 'mayan.apps.documents.workflow_actions.DocumentTypeChangeAction'
TEST_TRASH_DOCUMENT_WORKFLOW_ACTION_DOTTED_PATH = 'mayan.apps.documents.workflow_actions.TrashDocumentAction'
