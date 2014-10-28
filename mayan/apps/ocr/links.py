from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_OCR_CLEAN_ALL_PAGES,
                          PERMISSION_OCR_DOCUMENT,
                          PERMISSION_OCR_DOCUMENT_DELETE)

submit_document = {'text': _('Submit to OCR queue'), 'view': 'ocr:submit_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
submit_document_multiple = {'text': _('Submit to OCR queue'), 'view': 'ocr:submit_document_multiple', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
re_queue_document = {'text': _('Re-queue'), 'view': 'ocr:re_queue_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
re_queue_multiple_document = {'text': _('Re-queue'), 'view': 'ocr:re_queue_multiple_document', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
queue_document_delete = {'text': _(u'Delete'), 'view': 'ocr:queue_document_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}
queue_document_multiple_delete = {'text': _(u'Delete'), 'view': 'ocr:queue_document_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}

all_document_ocr_cleanup = {'text': _(u'Clean up pages content'), 'view': 'ocr:all_document_ocr_cleanup', 'famfam': 'text_strikethrough', 'permissions': [PERMISSION_OCR_CLEAN_ALL_PAGES], 'description': _(u'Runs a language filter to remove common OCR mistakes from document pages content.')}

queue_document_list = {'text': _(u'Queue document list'), 'view': 'ocr:queue_document_list', 'famfam': 'hourglass', 'permissions': [PERMISSION_OCR_DOCUMENT]}
ocr_tool_link = {'text': _(u'OCR'), 'view': 'ocr:queue_document_list', 'famfam': 'hourglass', 'icon': 'text.png', 'permissions': [PERMISSION_OCR_DOCUMENT]}
