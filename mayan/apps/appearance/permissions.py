from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Apparance'), name='apparance')

permission_theme_create = namespace.add_permission(
    label=_('Create new themes'), name='theme_create'
)
permission_theme_delete = namespace.add_permission(
    label=_('Delete themes'), name='theme_delete'
)
permission_theme_edit = namespace.add_permission(
    label=_('Edit themes'), name='theme_edit'
)
permission_theme_view = namespace.add_permission(
    label=_('View existing themes'), name='theme_view'
)
