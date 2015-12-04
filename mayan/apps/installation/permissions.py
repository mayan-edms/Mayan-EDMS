from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace('installation', _('Installation'))
permission_installation_details = namespace.add_permission(
    name='installation_details',
    label=_('View installation environment details')
)
