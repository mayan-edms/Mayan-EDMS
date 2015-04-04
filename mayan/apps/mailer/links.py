from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT

link_send_document_link = Link(permissions=[PERMISSION_MAILING_LINK], text=_('Email link'), view='mailer:send_document_link', args='object.pk')
link_send_document = Link(permissions=[PERMISSION_MAILING_SEND_DOCUMENT], text=_('Email document'), view='mailer:send_document', args='object.pk')
