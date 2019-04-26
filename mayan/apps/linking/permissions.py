from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Smart links'), name='linking')

permission_smart_link_create = namespace.add_permission(
    label=_('Create new smart links'), name='smart_link_create'
)
permission_smart_link_delete = namespace.add_permission(
    label=_('Delete smart links'), name='smart_link_delete'
)
permission_smart_link_edit = namespace.add_permission(
    label=_('Edit smart links'), name='smart_link_edit'
)
permission_smart_link_view = namespace.add_permission(
    label=_('View existing smart links'), name='smart_link_view'
)
