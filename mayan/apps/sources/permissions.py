from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

sources_setup_namespace = PermissionNamespace('sources_setup', _(u'Sources setup'))
PERMISSION_SOURCES_SETUP_VIEW = Permission.objects.register(sources_setup_namespace, 'sources_setup_view', _(u'View existing document sources'))
PERMISSION_SOURCES_SETUP_EDIT = Permission.objects.register(sources_setup_namespace, 'sources_setup_edit', _(u'Edit document sources'))
PERMISSION_SOURCES_SETUP_DELETE = Permission.objects.register(sources_setup_namespace, 'sources_setup_delete', _(u'Delete document sources'))
PERMISSION_SOURCES_SETUP_CREATE = Permission.objects.register(sources_setup_namespace, 'sources_setup_create', _(u'Create new document sources'))
