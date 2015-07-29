from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace('mailing', _('Mailing'))

permission_mailing_link = namespace.add_permission(
    name='mail_link', label=_('Send document link via email')
)
permission_mailing_send_document = namespace.add_permission(
    name='mail_document', label=_('Send document via email')
)
permission_view_error_log = namespace.add_permission(
    name='view_error_log', label=_('View document mailing error log')
)
