from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

events_namespace = PermissionNamespace('events', _('Events'))
PERMISSION_EVENTS_VIEW = Permission.objects.register(events_namespace, 'events_view', _('Access the events of an object'))
