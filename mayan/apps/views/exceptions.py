class BaseViewsException(Exception):
    """
    Base exception for the views app.
    """


class ActionError(BaseViewsException):
    """
    Raise by the MultiActionConfirmView to announce when the object action
    failed for one or more items.  This exception doesn't stop the iteration,
    it is used to announce that one item in the queryset failed to process.
    """
