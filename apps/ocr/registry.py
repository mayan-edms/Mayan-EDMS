from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .icons import icon_submit_document

label = _(u'OCR')
description = _(u'Handles optical character recognition.')
icon = icon_submit_document
dependencies = ['app_registry', 'icons', 'navigation']
settings = [
    {
        'name': 'TESSERACT_PATH',
        'default': u'/usr/bin/tesseract',
        'exists': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'TESSERACT_LANGUAGE',
        'default': u'eng',
        'scopes': [LocalScope()]
    },
    {
        'name': 'REPLICATION_DELAY',
        'default': 0,
        'description': _(u'Amount of seconds to delay OCR of documents to allow for the node\'s storage replication overhead.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'NODE_CONCURRENT_EXECUTION',
        'default': 1,
        'description': _(u'Maximum amount of concurrent document OCRs a node can perform.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'AUTOMATIC_OCR',
        'default': True,
        'description': _(u'Automatically queue newly created documents for OCR.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'QUEUE_PROCESSING_INTERVAL',
        'default': 10,
        'description': _(u'Automatically queue newly created documents for OCR.'),
        'scopes': [LocalScope()]
    },
    {
        'name': 'UNPAPER_PATH',
        'default': u'/usr/bin/unpaper',
        'description': _(u'File path to unpaper program.'),
        'exists': True,
        'scopes': [LocalScope()]
    },
    {
        'name': 'PDFTOTEXT_PATH',
        'default': u'/usr/bin/pdftotext',
        'description': _(u'File path to poppler\'s pdftotext program used to extract text from PDF files.'),
        'exists': True,
        'scopes': [LocalScope()]
    },
]
