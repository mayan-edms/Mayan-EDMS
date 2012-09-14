from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT

send_document_link = Link(text=_(u'email link'), view='send_document_link', args='object.pk', sprite='email_link', permissions=[PERMISSION_MAILING_LINK])
send_document = Link(text=_(u'email document'), view='send_document', args='object.pk', sprite='email_open', permissions=[PERMISSION_MAILING_SEND_DOCUMENT])
