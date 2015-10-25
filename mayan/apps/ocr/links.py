from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_document_type_ocr_setup
)

link_document_content = Link(
    permissions=(permission_ocr_content_view,), text=_('OCR'),
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
link_document_type_submit = Link(
    icon='fa fa-font', permissions=(permission_ocr_document,),
    text=_('OCR documents per type'), view='ocr:document_type_submit'
)
link_entry_list = Link(
    icon='fa fa-file-text-o', permissions=(permission_ocr_document,),
    text=_('OCR errors'), view='ocr:entry_list'
)
