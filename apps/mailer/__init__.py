from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links
from documents.models import Document
from acls.api import class_permissions

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT

send_document_link = {'text': _(u'email link'), 'view': 'send_document_link', 'args': 'object.pk', 'famfam': 'email_link', 'permissions': [PERMISSION_MAILING_LINK]}
send_document = {'text': _(u'email document'), 'view': 'send_document', 'args': 'object.pk', 'famfam': 'email_open', 'permissions': [PERMISSION_MAILING_SEND_DOCUMENT]}

register_links(Document, [send_document_link, send_document])

class_permissions(Document, [
    PERMISSION_MAILING_LINK,
    PERMISSION_MAILING_SEND_DOCUMENT
])
