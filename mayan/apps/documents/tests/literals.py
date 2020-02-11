# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings

from mayan.apps.common.literals import TIME_DELTA_UNIT_DAYS
from mayan.apps.converter.transformations import TransformationRotate

# Filenames
TEST_COMPRESSED_DOCUMENTS_FILENAME = 'compressed_documents.zip'
TEST_DEU_DOCUMENT_FILENAME = 'deu_website.png'
TEST_DOCUMENT_DESCRIPTION = 'test description'
TEST_DOCUMENT_DESCRIPTION_EDITED = 'test document description edited'
TEST_DOCUMENT_LABEL_EDITED = 'test document label edited'
TEST_DOCUMENT_TYPE_DELETE_PERIOD = 30
TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT = TIME_DELTA_UNIT_DAYS
TEST_DOCUMENT_TYPE_LABEL = 'test_document_type'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2'
TEST_DOCUMENT_TYPE_LABEL_EDITED = 'test document type edited label'
TEST_DOCUMENT_TYPE_QUICK_LABEL = 'test quick label'
TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED = 'test quick label edited'
TEST_DOCUMENT_VERSION_COMMENT_EDITED = 'test document version comment edited'
TEST_HYBRID_DOCUMENT = 'hybrid_text_and_image.pdf'
TEST_MULTI_PAGE_TIFF = 'multi_page.tiff'
TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png.zip'
TEST_NON_ASCII_DOCUMENT_FILENAME = 'I18N_title_áéíóúüñÑ.png'
TEST_OFFICE_DOCUMENT = 'simple_2_page_document.doc'
TEST_PDF_DOCUMENT_FILENAME = 'mayan_11_1.pdf'
TEST_PDF_INDIRECT_ROTATE_LABEL = 'indirect_rotate.pdf'
TEST_PDF_ROTATE_ALTERNATE_LABEL = 'rotate_alternate.pdf'
TEST_SMALL_DOCUMENT_FILENAME = 'title_page.png'
TEST_SMALL_DOCUMENT_CHECKSUM = 'efa10e6cc21f83078aaa94d5cbe51de67b51af706143b\
afc7fd6d4c02124879a'
TEST_SMALL_DOCUMENT_MIMETYPE = 'image/png'
TEST_SMALL_DOCUMENT_SIZE = 17436
TEST_TRANSFORMATION_CLASS = TransformationRotate
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'

# File paths
TEST_COMPRESSED_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_COMPRESSED_DOCUMENTS_FILENAME
)
TEST_DEU_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_DEU_DOCUMENT_FILENAME
)
TEST_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_PDF_DOCUMENT_FILENAME
)
TEST_HYBRID_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_HYBRID_DOCUMENT
)
TEST_MULTI_PAGE_TIFF_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_MULTI_PAGE_TIFF
)
TEST_NON_ASCII_COMPRESSED_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_NON_ASCII_COMPRESSED_DOCUMENT_FILENAME
)
TEST_NON_ASCII_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_NON_ASCII_DOCUMENT_FILENAME
)
TEST_PDF_INDIRECT_ROTATE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_PDF_INDIRECT_ROTATE_LABEL
)
TEST_PDF_ROTATE_ALTERNATE_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_PDF_ROTATE_ALTERNATE_LABEL
)
TEST_OFFICE_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_OFFICE_DOCUMENT
)
TEST_SMALL_DOCUMENT_PATH = os.path.join(
    settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
    'sample_documents', TEST_SMALL_DOCUMENT_FILENAME
)
TEST_VERSION_COMMENT = 'test version comment'
