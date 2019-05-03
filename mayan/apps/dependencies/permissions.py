from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Dependencies'), name='dependencies')

permission_dependencies_view = namespace.add_permission(
    label=_('View dependencies'), name='dependencies_view'
)
