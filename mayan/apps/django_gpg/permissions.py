from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Key management'), name='django_gpg')

permission_key_delete = namespace.add_permission(
    label=_('Delete keys'), name='key_delete'
)
permission_key_download = namespace.add_permission(
    label=_('Download keys'), name='key_download'
)
permission_key_receive = namespace.add_permission(
    label=_('Import keys from keyservers'), name='key_receive'
)
permission_key_sign = namespace.add_permission(
    label=_('Use keys to sign content'), name='key_sign'
)
permission_key_upload = namespace.add_permission(
    label=_('Upload keys'), name='key_upload'
)
permission_key_view = namespace.add_permission(
    label=_('View keys'), name='key_view'
)
permission_keyserver_query = namespace.add_permission(
    label=_('Query keyservers'), name='keyserver_query'
)
