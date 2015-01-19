from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('checkouts', _('Document checkout'))

PERMISSION_DOCUMENT_CHECKOUT = Permission.objects.register(namespace, 'checkout_document', _('Check out documents'))
PERMISSION_DOCUMENT_CHECKIN = Permission.objects.register(namespace, 'checkin_document', _('Check in documents'))
PERMISSION_DOCUMENT_CHECKIN_OVERRIDE = Permission.objects.register(namespace, 'checkin_document_override', _('Forcefully check in documents'))
PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE = Permission.objects.register(namespace, 'checkout_restrictions_override', _('Allow overriding check out restrictions'))
