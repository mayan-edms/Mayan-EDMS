from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_OCR_CONTENT_VIEW, PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE
)

link_document_content = Link(permissions=[PERMISSION_OCR_CONTENT_VIEW], text=_('Content'), view='ocr:document_content', args='resolved_object.id')
link_document_submit = Link(permissions=[PERMISSION_OCR_DOCUMENT], text=_('Submit to OCR queue'), view='ocr:document_submit', args='object.id')
link_document_submit_multiple = Link(text=_('Submit to OCR queue'), view='ocr:document_submit_multiple')
link_entry_delete = Link(permissions=[PERMISSION_OCR_DOCUMENT_DELETE], text=_('Delete'), view='ocr:entry_delete', args='object.id')
link_entry_delete_multiple = Link(text=_('Delete'), view='ocr:entry_delete_multiple')
link_entry_list = Link(icon='fa fa-file-text-o', permissions=[PERMISSION_OCR_DOCUMENT], text=_('OCR Errors'), view='ocr:entry_list')
link_entry_re_queue = Link(permissions=[PERMISSION_OCR_DOCUMENT], text=_('Re-queue'), view='ocr:entry_re_queue', args='object.id')
link_entry_re_queue_multiple = Link(text=_('Re-queue'), view='ocr:entry_re_queue_multiple')
