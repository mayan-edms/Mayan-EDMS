from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace(
    'document_signatures', _('Document signatures')
)

permission_document_verify = namespace.add_permission(
    name='document_verify', label=_('Verify document signatures')
)
permission_signature_delete = namespace.add_permission(
    name='signature_delete', label=_('Delete detached signatures')
)
permission_signature_download = namespace.add_permission(
    name='signature_download', label=_('Download detached signatures')
)
permission_signature_upload = namespace.add_permission(
    name='signature_upload', label=_('Upload detached signatures')
)
