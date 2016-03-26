from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace(
    'document_signatures', _('Document signatures')
)

permission_document_version_signature_view = namespace.add_permission(
    name='document_version_signature_view',
    label=_('View details of document signatures')
)
permission_document_version_signature_delete = namespace.add_permission(
    name='document_version_signature_delete',
    label=_('Delete detached signatures')
)
permission_document_version_signature_download = namespace.add_permission(
    name='document_version_signature_download',
    label=_('Download detached document signatures')
)
permission_document_version_signature_upload = namespace.add_permission(
    name='document_version_signature_upload',
    label=_('Upload detached document signatures')
)
