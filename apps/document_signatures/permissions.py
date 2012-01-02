from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.api import register_permission, set_namespace_title
from permissions.models import PermissionNamespace, Permission

document_signatures_namespace = PermissionNamespace('document_signatures', _(u'Document signatures'))

PERMISSION_DOCUMENT_VERIFY = Permission.objects.register(document_signatures_namespace, 'document_verify', _(u'Verify document signatures'))
PERMISSION_SIGNATURE_UPLOAD = Permission.objects.register(document_signatures_namespace, 'signature_upload', _(u'Upload detached signatures'))
PERMISSION_SIGNATURE_DOWNLOAD = Permission.objects.register(document_signatures_namespace, 'signature_download', _(u'Download detached signatures'))
