from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Tags'), name='tags')

permission_tag_create = namespace.add_permission(
    label=_('Create new tags'), name='tag_create'
)
permission_tag_delete = namespace.add_permission(
    label=_('Delete tags'), name='tag_delete'
)
permission_tag_view = namespace.add_permission(
    label=_('View tags'), name='tag_view'
)
permission_tag_edit = namespace.add_permission(
    label=_('Edit tags'), name='tag_edit'
)
permission_tag_attach = namespace.add_permission(
    label=_('Attach tags to documents'), name='tag_attach'
)
permission_tag_remove = namespace.add_permission(
    label=_('Remove tags from documents'), name='tag_remove'
)
