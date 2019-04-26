from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Document checkout'), name='checkouts')

permission_document_check_in = namespace.add_permission(
    label=_('Check in documents'), name='checkin_document'
)
permission_document_check_in_override = namespace.add_permission(
    label=_('Forcefully check in documents'), name='checkin_document_override'
)
permission_document_check_out = namespace.add_permission(
    label=_('Check out documents'), name='checkout_document'
)
permission_document_check_out_detail_view = namespace.add_permission(
    label=_('Check out details view'), name='checkout_detail_view'
)
