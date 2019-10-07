from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_document_type_ocr_setup
)

link_document_page_ocr_content = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_page_ocr_content',
    permissions=(permission_ocr_content_view,), text=_('OCR'),
    view='ocr:document_page_ocr_content',
)
link_document_ocr_content = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_ocr_content',
    permissions=(permission_ocr_content_view,), text=_('OCR'),
    view='ocr:document_ocr_content',
)
link_document_ocr_content_delete = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_ocr_content_delete',
    permissions=(permission_ocr_content_view,), text=_('Delete OCR content'),
    view='ocr:document_ocr_content_delete',
)
link_document_ocr_content_delete_multiple = Link(
    icon_class_path='mayan.apps.ocr.icons.icon_document_ocr_content_delete',
    text=_('Delete OCR content'),
    view='ocr:document_ocr_content_delete_multiple',
)
link_document_submit = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_submit',
    permissions=(permission_ocr_document,), text=_('Submit for OCR'),
    view='ocr:document_submit'
)
link_document_submit_multiple = Link(
    icon_class_path='mayan.apps.ocr.icons.icon_document_submit',
    text=_('Submit for OCR'), view='ocr:document_submit_multiple'
)
link_document_type_ocr_settings = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_type_ocr_settings',
    permissions=(permission_document_type_ocr_setup,), text=_('Setup OCR'),
    view='ocr:document_type_ocr_settings',
)
link_document_type_submit = Link(
    icon_class_path='mayan.apps.ocr.icons.icon_document_type_submit',
    permissions=(permission_ocr_document,), text=_('OCR documents per type'),
    view='ocr:document_type_submit'
)
link_entry_list = Link(
    icon_class_path='mayan.apps.ocr.icons.icon_entry_list',
    permissions=(permission_ocr_document,), text=_('OCR errors'),
    view='ocr:entry_list'
)
link_document_ocr_errors_list = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_ocr_errors_list',
    permissions=(permission_ocr_content_view,), text=_('OCR errors'),
    view='ocr:document_ocr_error_list'
)
link_document_ocr_download = Link(
    args='resolved_object.id',
    icon_class_path='mayan.apps.ocr.icons.icon_document_ocr_download',
    permissions=(permission_ocr_content_view,), text=_('Download OCR text'),
    view='ocr:document_ocr_download'
)
