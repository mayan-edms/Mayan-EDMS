from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace('folders', _('Folders'))

permission_folder_create = namespace.add_permission(
    name='folder_create', label=_('Create folders')
)
permission_folder_edit = namespace.add_permission(
    name='folder_edit', label=_('Edit folders')
)
permission_folder_delete = namespace.add_permission(
    name='folder_delete', label=_('Delete folders')
)
permission_folder_remove_document = namespace.add_permission(
    name='folder_remove_document', label=_('Remove documents from folders')
)
permission_folder_view = namespace.add_permission(
    name='folder_view', label=_('View folders')
)
# Translators: this refers to the permission that will allow users to add
# documents to folders.
permission_folder_add_document = namespace.add_permission(
    name='folder_add_document', label=_('Add documents to folders')
)
