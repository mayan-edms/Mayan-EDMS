from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Sources setup'), name='sources_setup')

permission_sources_setup_create = namespace.add_permission(
    label=_('Create new document sources'), name='sources_setup_create'
)
permission_sources_setup_delete = namespace.add_permission(
    label=_('Delete document sources'), name='sources_setup_delete'
)
permission_sources_setup_edit = namespace.add_permission(
    label=_('Edit document sources'), name='sources_setup_edit'
)
permission_sources_setup_view = namespace.add_permission(
    label=_('View existing document sources'), name='sources_setup_view'
)
permission_staging_file_delete = namespace.add_permission(
    label=_('Delete staging files'), name='sources_staging_file_delete'
)
