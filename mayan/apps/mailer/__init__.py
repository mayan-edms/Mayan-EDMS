from acls.api import class_permissions
from documents.models import Document
from navigation.api import register_links

from .links import send_document_link, send_document
from .permissions import (
    PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
)

register_links([Document], [send_document_link, send_document])

class_permissions(Document, [
    PERMISSION_MAILING_LINK, PERMISSION_MAILING_SEND_DOCUMENT
])
