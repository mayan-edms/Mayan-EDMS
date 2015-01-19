from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

django_gpg_namespace = PermissionNamespace('django_gpg', _('Key management'))

PERMISSION_KEY_VIEW = Permission.objects.register(django_gpg_namespace, 'key_view', _('View keys'))
PERMISSION_KEY_DELETE = Permission.objects.register(django_gpg_namespace, 'key_delete', _('Delete keys'))
PERMISSION_KEYSERVER_QUERY = Permission.objects.register(django_gpg_namespace, 'keyserver_query', _('Query keyservers'))
PERMISSION_KEY_RECEIVE = Permission.objects.register(django_gpg_namespace, 'key_receive', _('Import keys from keyservers'))
