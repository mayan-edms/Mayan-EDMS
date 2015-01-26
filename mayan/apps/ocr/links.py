from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .permissions import (
    PERMISSION_OCR_CLEAN_ALL_PAGES, PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE
)

link_document_submit = {'text': _('Submit to OCR queue'), 'view': 'ocr:document_submit', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
link_document_submit_multiple = {'text': _('Submit to OCR queue'), 'view': 'ocr:document_submit_multiple', 'famfam': 'hourglass_add'}
link_entry_re_queue = {'text': _('Re-queue'), 'view': 'ocr:entry_re_queue', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
link_entry_re_queue_multiple = {'text': _('Re-queue'), 'view': 'ocr:entry_re_queue_multiple', 'famfam': 'hourglass_add'}
link_entry_delete = {'text': _('Delete'), 'view': 'ocr:entry_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}
link_entry_delete_multiple = {'text': _('Delete'), 'view': 'ocr:entry_delete_multiple', 'famfam': 'hourglass_delete'}

link_document_all_ocr_cleanup = {'text': _('Clean up pages content'), 'view': 'ocr:document_all_ocr_cleanup', 'famfam': 'text_strikethrough', 'permissions': [PERMISSION_OCR_CLEAN_ALL_PAGES], 'description': _('Runs a language filter to remove common OCR mistakes from document pages content.')}

link_entry_list = {'text': _('OCR Errors'), 'view': 'ocr:entry_list', 'famfam': 'hourglass', 'icon': 'main/icons/text.png', 'permissions': [PERMISSION_OCR_DOCUMENT]}
