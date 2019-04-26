from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Common'), name='common')

permission_error_log_view = namespace.add_permission(
    label=_('View error log'), name='error_log_view'
)
