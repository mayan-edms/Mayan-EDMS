from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Comments'), name='comments')

permission_comment_create = namespace.add_permission(
    label=_('Create new comments'), name='comment_create'
)
permission_comment_delete = namespace.add_permission(
    label=_('Delete comments'), name='comment_delete'
)
permission_comment_view = namespace.add_permission(
    label=_('View comments'), name='comment_view'
)
