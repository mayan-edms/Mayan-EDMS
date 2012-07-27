from __future__ import absolute_import

from navigation.api import bind_links
from documents.models import Document
from acls.api import class_permissions

from .permissions import PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
from .links import send_document_link, send_document

bind_links([Document], [send_document_link, send_document])

class_permissions(Document, [
    PERMISSION_MAILING_LINK,
    PERMISSION_MAILING_SEND_DOCUMENT
])
