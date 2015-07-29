from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_view_error_log
)

link_send_document = Link(
    permissions=(permission_mailing_send_document,), text=_('Email document'),
    view='mailer:send_document', args='object.pk'
)
link_send_document_link = Link(
    permissions=(permission_mailing_link,), text=_('Email link'),
    view='mailer:send_document_link', args='object.pk'
)
link_document_mailing_error_log = Link(
    icon='fa fa-envelope', permissions=(permission_view_error_log,),
    text=_('Document mailing error log'), view='mailer:error_log',
)
