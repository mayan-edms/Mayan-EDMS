from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

document_signatures_namespace = PermissionNamespace('document_signatures', _('Document signatures'))
PERMISSION_DOCUMENT_VERIFY = Permission.objects.register(document_signatures_namespace, 'document_verify', _('Verify document signatures'))
PERMISSION_SIGNATURE_DELETE = Permission.objects.register(document_signatures_namespace, 'signature_delete', _('Delete detached signatures'))
PERMISSION_SIGNATURE_DOWNLOAD = Permission.objects.register(document_signatures_namespace, 'signature_download', _('Download detached signatures'))
PERMISSION_SIGNATURE_UPLOAD = Permission.objects.register(document_signatures_namespace, 'signature_upload', _('Upload detached signatures'))
