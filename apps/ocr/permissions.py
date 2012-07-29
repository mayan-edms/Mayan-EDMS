from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

ocr_namespace = PermissionNamespace('ocr', _(u'OCR'))
PERMISSION_OCR_DOCUMENT = Permission.objects.register(ocr_namespace, 'ocr_document', _(u'Submit documents for OCR'))
PERMISSION_OCR_DOCUMENT_DELETE = Permission.objects.register(ocr_namespace, 'ocr_document_delete', _(u'Delete documents from OCR queue'))
PERMISSION_OCR_QUEUE_ENABLE_DISABLE = Permission.objects.register(ocr_namespace, 'ocr_queue_enable_disable', _(u'Can enable/disable the OCR processing'))
PERMISSION_OCR_CLEAN_ALL_PAGES = Permission.objects.register(ocr_namespace, 'ocr_clean_all_pages', _(u'Can execute the OCR clean up on all document pages'))
PERMISSION_OCR_QUEUE_EDIT = Permission.objects.register(ocr_namespace, 'ocr_queue_edit', _(u'Can edit an OCR queue properties'))
