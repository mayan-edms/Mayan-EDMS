from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

sources_setup_namespace = PermissionNamespace('sources_setup', _('Sources setup'))
PERMISSION_SOURCES_SETUP_CREATE = Permission.objects.register(sources_setup_namespace, 'sources_setup_create', _('Create new document sources'))
PERMISSION_SOURCES_SETUP_DELETE = Permission.objects.register(sources_setup_namespace, 'sources_setup_delete', _('Delete document sources'))
PERMISSION_SOURCES_SETUP_EDIT = Permission.objects.register(sources_setup_namespace, 'sources_setup_edit', _('Edit document sources'))
PERMISSION_SOURCES_SETUP_VIEW = Permission.objects.register(sources_setup_namespace, 'sources_setup_view', _('View existing document sources'))
