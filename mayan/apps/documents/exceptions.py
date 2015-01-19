from __future__ import unicode_literals


class NewDocumentVersionNotAllowed(Exception):
    """
    Uploading new versions for this document is not allowed
    Current reasons:  Document is in checked out state
    """
    pass
