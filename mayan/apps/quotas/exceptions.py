
class QuotaBaseException(Exception):
    """Base exception for the quota app"""


class QuotaExceeded(QuotaBaseException):
    """Raised when a quota allocation is exceeded"""
