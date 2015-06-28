from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

acls_namespace = PermissionNamespace('acls', _('Access control lists'))
acls_setup_namespace = PermissionNamespace('acls_setup', _('Access control lists'))

acls_edit_acl = acls_namespace.add_permission(name='acl_edit', label=_('Edit ACLs'))
acls_view_acl = acls_namespace.add_permission(name='acl_view', label=_('View ACLs'))

acls_class_edit_acl = acls_setup_namespace.add_permission(name='acl_class_edit', label=_('Edit class default ACLs'))
acls_class_view_acl = acls_setup_namespace.add_permission(name='acl_class_view', label=_('View class default ACLs'))
