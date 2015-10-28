from __future__ import unicode_literals


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
