"""Configuration options for the ocr app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('ocr', _(u'OCR'), module='ocr.conf.settings')

Setting(
    namespace=namespace,
    name='TESSERACT_PATH',
    global_name='OCR_TESSERACT_PATH',
    default=u'/usr/bin/tesseract',
    exists=True,
)

Setting(
    namespace=namespace,
    name='TESSERACT_LANGUAGE',
    global_name='OCR_TESSERACT_LANGUAGE',
    default=u'eng',
)

Setting(
    namespace=namespace,
    name='REPLICATION_DELAY',
    global_name='OCR_REPLICATION_DELAY',
    default=0,
    description=_(u'Amount of seconds to delay OCR of documents to allow for the node\'s storage replication overhead.'),
)

Setting(
    namespace=namespace,
    name='NODE_CONCURRENT_EXECUTION',
    global_name='OCR_NODE_CONCURRENT_EXECUTION',
    default=1,
    description=_(u'Maximum amount of concurrent document OCRs a node can perform.')
)

Setting(
    namespace=namespace,
    name='AUTOMATIC_OCR',
    global_name='OCR_AUTOMATIC_OCR',
    default=False,
    description=_(u'Automatically queue newly created documents for OCR.')
)

Setting(
    namespace=namespace,
    name='QUEUE_PROCESSING_INTERVAL',
    global_name='OCR_QUEUE_PROCESSING_INTERVAL',
    default=10,
    description=_(u'Automatically queue newly created documents for OCR.')
)

Setting(
    namespace=namespace,
    name='UNPAPER_PATH',
    global_name='OCR_UNPAPER_PATH',
    default=u'/usr/bin/unpaper',
    description=_(u'File path to unpaper program.'),
    exists=True
)

Setting(
    namespace=namespace,
    name='PDFTOTEXT_PATH',
    global_name='OCR_PDFTOTEXT_PATH',
    default=u'/usr/bin/pdftotext',
    description=_(u'File path to poppler\'s pdftotext program used to extract text from PDF files.'),
    exists=True
)
