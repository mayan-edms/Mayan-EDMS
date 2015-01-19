from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT

send_document_link = {'text': _('Email link'), 'view': 'mailer:send_document_link', 'args': 'object.pk', 'famfam': 'email_link', 'permissions': [PERMISSION_MAILING_LINK]}
send_document = {'text': _('Email document'), 'view': 'mailer:send_document', 'args': 'object.pk', 'famfam': 'email_open', 'permissions': [PERMISSION_MAILING_SEND_DOCUMENT]}
