from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

ocr_namespace = PermissionNamespace('ocr', _('OCR'))
PERMISSION_OCR_DOCUMENT = Permission.objects.register(ocr_namespace, 'ocr_document', _('Submit documents for OCR'))
PERMISSION_OCR_DOCUMENT_DELETE = Permission.objects.register(ocr_namespace, 'ocr_document_delete', _('Delete documents from OCR queue'))
PERMISSION_OCR_CLEAN_ALL_PAGES = Permission.objects.register(ocr_namespace, 'ocr_clean_all_pages', _('Can execute the OCR clean up on all document pages'))
