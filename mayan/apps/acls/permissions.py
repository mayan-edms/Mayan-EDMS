from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

acls_namespace = PermissionNamespace('acls', _('Access control lists'))
acls_setup_namespace = PermissionNamespace('acls_setup', _('Access control lists'))

ACLS_EDIT_ACL = Permission.objects.register(acls_namespace, 'acl_edit', _('Edit ACLs'))
ACLS_VIEW_ACL = Permission.objects.register(acls_namespace, 'acl_view', _('View ACLs'))

ACLS_CLASS_EDIT_ACL = Permission.objects.register(acls_setup_namespace, 'acl_class_edit', _('Edit class default ACLs'))
ACLS_CLASS_VIEW_ACL = Permission.objects.register(acls_setup_namespace, 'acl_class_view', _('View class default ACLs'))
