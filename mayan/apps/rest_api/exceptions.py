
class APIError(Exception):
    """
    Base exception for the API app.
    """


class APIResourcePatternError(APIError):
    """
    Raised when an app tries to override an existing URL regular expression
    pattern.
    """
