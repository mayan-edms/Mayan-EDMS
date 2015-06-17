from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

ocr_namespace = PermissionNamespace('ocr', _('OCR'))
PERMISSION_OCR_DOCUMENT = Permission.objects.register(ocr_namespace, 'ocr_document', _('Submit documents for OCR'))
PERMISSION_OCR_DOCUMENT_DELETE = Permission.objects.register(ocr_namespace, 'ocr_document_delete', _('Delete documents from OCR queue'))
PERMISSION_OCR_CONTENT_VIEW = Permission.objects.register(ocr_namespace, 'ocr_content_view', _('Can view the transcribed text from document'))
