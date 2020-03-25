from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Converter'), name='converter')

permission_transformation_create = namespace.add_permission(
    label=_('Create new transformations'), name='transformation_create'
)
permission_transformation_delete = namespace.add_permission(
    label=_('Delete transformations'), name='transformation_delete'
)
permission_transformation_edit = namespace.add_permission(
    label=_('Edit transformations'), name='transformation_edit'
)
permission_transformation_view = namespace.add_permission(
    label=_('View existing transformations'), name='transformation_view'
)
