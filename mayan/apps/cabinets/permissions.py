from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Cabinets'), name='cabinets')

# Translators: this refers to the permission that will allow users to add
# documents to cabinets.
permission_cabinet_add_document = namespace.add_permission(
    label=_('Add documents to cabinets'), name='cabinet_add_document'
)
permission_cabinet_create = namespace.add_permission(
    label=_('Create cabinets'), name='cabinet_create'
)
permission_cabinet_delete = namespace.add_permission(
    label=_('Delete cabinets'), name='cabinet_delete'
)
permission_cabinet_edit = namespace.add_permission(
    label=_('Edit cabinets'), name='cabinet_edit'
)
permission_cabinet_remove_document = namespace.add_permission(
    label=_('Remove documents from cabinets'), name='cabinet_remove_document'
)
permission_cabinet_view = namespace.add_permission(
    label=_('View cabinets'), name='cabinet_view'
)
