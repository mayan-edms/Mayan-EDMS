from __future__ import unicode_literals

from django.utils.translation import ugettext


class DocumentException(Exception):
    """
    Base documents warning
    """
    pass


class NewDocumentVersionNotAllowed(DocumentException):
    """
    Uploading new versions for this document is not allowed
    """
    pass
