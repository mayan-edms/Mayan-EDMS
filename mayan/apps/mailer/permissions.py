from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

mailer_namespace = PermissionNamespace('mailing', _('Mailing'))

PERMISSION_MAILING_LINK = Permission.objects.register(mailer_namespace, 'mail_link', _('Send document link via email'))
PERMISSION_MAILING_SEND_DOCUMENT = Permission.objects.register(mailer_namespace, 'mail_document', _('Send document via email'))
