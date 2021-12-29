class DynamicSearchException(Exception):
    """
    Base exception for the app.
    """


class DynamicSearchRetry(DynamicSearchException):
    """
    Exception to encapsulate backend specific errors that should be retried.
    """
