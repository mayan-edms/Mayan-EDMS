from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope, ClusterScope

from .icons import icon_submit_document
from .literals import (DEFAULT_TESSERACT_PATH, DEFAULT_TESSERACT_LANGUAGE,
    DEFAULT_REPLICATION_DELAY, DEFAULT_UNPAPER_PATH, DEFAULT_PDFTOTEXT_PATH)
from .links import all_document_ocr_cleanup

label = _(u'OCR')
description = _(u'Handles optical character recognition.')
icon = icon_submit_document
dependencies = ['app_registry', 'icons', 'navigation']
#maintenance_links = [all_document_ocr_cleanup]
settings = [
    {
        'name': 'AUTOMATIC_OCR',
        'default': True,
        'description': _(u'Automatically queue newly created documents for OCR.'),
        'scopes': [ClusterScope()]
    },
    {
        'name': 'TESSERACT_PATH',
        'default': DEFAULT_TESSERACT_PATH,
        'exists': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'TESSERACT_LANGUAGE',
        'default': DEFAULT_TESSERACT_LANGUAGE,
        'scopes': [ClusterScope()]
    },
    {
        'name': 'REPLICATION_DELAY',
        'default': DEFAULT_REPLICATION_DELAY,
        'description': _(u'Amount of seconds to delay OCR of documents to allow for the node\'s storage replication overhead.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'UNPAPER_PATH',
        'default': DEFAULT_UNPAPER_PATH,
        'description': _(u'File path to unpaper program.'),
        'exists': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'PDFTOTEXT_PATH',
        'default': DEFAULT_PDFTOTEXT_PATH,
        'description': _(u'File path to poppler\'s pdftotext program used to extract text from PDF files.'),
        'exists': True,
        'scopes': [LocalScope()]
    },
]
