from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_mailing_link, permission_mailing_send_document
)

link_send_document = Link(
    permissions=(permission_mailing_send_document,), text=_('Email document'),
    view='mailer:send_document', args='object.pk'
)
link_send_document_link = Link(
    permissions=(permission_mailing_link,), text=_('Email link'),
    view='mailer:send_document_link', args='object.pk'
)
