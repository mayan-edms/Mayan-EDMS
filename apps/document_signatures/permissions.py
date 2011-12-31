from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.api import register_permission, set_namespace_title

PERMISSION_DOCUMENT_VERIFY = {'namespace': 'document_signatures', 'name': 'document_verify', 'label': _(u'Verify document signatures')}
PERMISSION_SIGNATURE_UPLOAD = {'namespace': 'document_signatures', 'name': 'signature_upload', 'label': _(u'Upload detached signatures')}
PERMISSION_SIGNATURE_DOWNLOAD = {'namespace': 'document_signatures', 'name': 'key_receive', 'label': _(u'Download detached signatures')}

# Permission setup
set_namespace_title('document_signatures', _(u'Document signatures'))
register_permission(PERMISSION_DOCUMENT_VERIFY)
register_permission(PERMISSION_SIGNATURE_UPLOAD)
register_permission(PERMISSION_SIGNATURE_DOWNLOAD)
