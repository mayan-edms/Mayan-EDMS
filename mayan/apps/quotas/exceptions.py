from __future__ import unicode_literals


class QuotaBaseException(Exception):
    """
    Base exception for the quota app
    """
    pass


class QuotaExceeded(QuotaBaseException):
    pass
