from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

mailer_namespace = PermissionNamespace('mailing', _(u'Mailing'))

PERMISSION_MAILING_LINK = Permission.objects.register(mailer_namespace, 'mail_link', _(u'Send document link via email'))
PERMISSION_MAILING_SEND_DOCUMENT = Permission.objects.register(mailer_namespace, 'mail_document', _(u'Send document via email'))
