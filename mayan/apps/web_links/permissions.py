from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Web links'), name='web_links')

permission_web_link_create = namespace.add_permission(
    label=_('Create new web links'), name='web_link_create'
)
permission_web_link_delete = namespace.add_permission(
    label=_('Delete web links'), name='web_link_delete'
)
permission_web_link_edit = namespace.add_permission(
    label=_('Edit web links'), name='web_link_edit'
)
permission_web_link_view = namespace.add_permission(
    label=_('View existing web links'), name='web_link_view'
)
permission_web_link_instance_view = namespace.add_permission(
    label=_('View web link instances'), name='web_link_instance_view'
)
