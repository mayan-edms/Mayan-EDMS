from __future__ import unicode_literals


class APIError(Exception):
    """
    Base exception for the API app
    """
    pass


class APIResourcePatternError(APIError):
    """
    Raised when an app tries to override an existing URL regular expression
    pattern
    """
    pass
