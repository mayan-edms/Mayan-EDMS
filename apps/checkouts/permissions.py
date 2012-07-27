from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('checkouts', _(u'Document checkout'))

PERMISSION_DOCUMENT_CHECKOUT = Permission.objects.register(namespace, 'checkout_document', _(u'Check out documents'))
PERMISSION_DOCUMENT_CHECKIN = Permission.objects.register(namespace, 'checkin_document', _(u'Check in documents'))
PERMISSION_DOCUMENT_CHECKIN_OVERRIDE = Permission.objects.register(namespace, 'checkin_document_override', _(u'Forcefully check in documents'))
PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE = Permission.objects.register(namespace, 'checkout_restrictions_override', _(u'Allow overriding check out restrictions'))
