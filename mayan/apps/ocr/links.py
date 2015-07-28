from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_ocr_document_delete, permission_document_type_ocr_setup
)

link_document_content = Link(
    permissions=(permission_ocr_content_view,), text=_('Content'),
    view='ocr:document_content', args='resolved_object.id'
)
link_document_submit = Link(
    permissions=(permission_ocr_document,), text=_('Submit for OCR'),
    view='ocr:document_submit', args='object.id'
)
link_document_submit_all = Link(
    icon='fa fa-font', permissions=(permission_ocr_document,),
    text=_('OCR all documents'), view='ocr:document_submit_all'
)
link_document_submit_multiple = Link(
    text=_('Submit for OCR'), view='ocr:document_submit_multiple'
)
link_document_type_ocr_settings = Link(
    permissions=(permission_document_type_ocr_setup,), text=_('Setup OCR'),
    view='ocr:document_type_ocr_settings', args='resolved_object.id'
)
link_entry_delete = Link(
    permissions=(permission_ocr_document_delete,), text=_('Delete'),
    view='ocr:entry_delete', args='object.id'
)
link_entry_delete_multiple = Link(
    text=_('Delete'), view='ocr:entry_delete_multiple'
)
link_entry_list = Link(
    icon='fa fa-file-text-o', permissions=(permission_ocr_document,),
    text=_('OCR errors'), view='ocr:entry_list'
)
link_entry_re_queue = Link(
    permissions=(permission_ocr_document,), text=_('Re-queue'),
    view='ocr:entry_re_queue', args='object.id'
)
link_entry_re_queue_multiple = Link(
    text=_('Re-queue'), view='ocr:entry_re_queue_multiple'
)
