from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Messaging'), name='messaging')

permission_message_create = namespace.add_permission(
    label=_('Create messages'), name='message_create'
)
permission_message_delete = namespace.add_permission(
    label=_('Delete messages'), name='message_delete'
)
permission_message_view = namespace.add_permission(
    label=_('View messages'), name='message_view'
)
