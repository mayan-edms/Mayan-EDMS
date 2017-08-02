from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace('quotas', _('Quotas'))

permission_quota_create = namespace.add_permission(
    name='quota_create', label=_('Create a quota')
)
permission_quota_delete = namespace.add_permission(
    name='quota_delete', label=_('Delete a quota')
)
permission_quota_edit = namespace.add_permission(
    name='quota_edit', label=_('Edit a quota')
)
permission_quota_view = namespace.add_permission(
    name='quota_view', label=_('View a quota')
)
