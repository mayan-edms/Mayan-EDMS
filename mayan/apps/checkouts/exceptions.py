from __future__ import unicode_literals

from django.utils.translation import ugettext


class DocumentCheckoutError(Exception):
    """
    Base checkout exception
    """
    pass


class DocumentNotCheckedOut(DocumentCheckoutError):
    """
    Raised when trying to checkin a document that is not checkedout
    """
    pass


class DocumentAlreadyCheckedOut(DocumentCheckoutError):
    """
    Raised when trying to checkout an already checkedout document
    """
    def __unicode__(self):
        return ugettext('Document already checked out.')
