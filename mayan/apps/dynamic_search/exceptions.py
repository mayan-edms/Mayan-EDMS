class DynamicSearchException(Exception):
    """
    Base exception for the app.
    """


class DynamicSearchRetry(DynamicSearchException):
    """
    Exception to encapsulate backend specific error that should be retried.
    """
