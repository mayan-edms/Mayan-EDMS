from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('installation', _('Installation'))
PERMISSION_INSTALLATION_DETAILS = Permission.objects.register(namespace, 'installation_details', _('View installation environment details'))
