from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE, PERMISSION_OCR_QUEUE_ENABLE_DISABLE,
    PERMISSION_OCR_CLEAN_ALL_PAGES)
from .icons import icon_submit_document, icon_ocr_cleanup
 
submit_document = Link(text=_('submit to OCR queue'), view='submit_document', args='object.id', icon=icon_submit_document, permissions=[PERMISSION_OCR_DOCUMENT])
submit_document_multiple = Link(text=_('submit to OCR queue'), view='submit_document_multiple', icon=icon_submit_document, permissions=[PERMISSION_OCR_DOCUMENT])

all_document_ocr_cleanup = Link(text=_(u'clean up pages content'), view='all_document_ocr_cleanup', icon=icon_ocr_cleanup, permissions=[PERMISSION_OCR_CLEAN_ALL_PAGES], description=_(u'Runs a language filter to remove common OCR mistakes from document pages content.'))
