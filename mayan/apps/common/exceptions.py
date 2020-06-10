class BaseCommonException(Exception):
    """
    Base exception for the common app
    """
    pass


class ActionError(BaseCommonException):
    """
    Raise by the MultiActionConfirmView to announce when the object action
    failed for one or more items.  This exception doesn't stop the iteration,
    it is used to announce that one item in the queryset failed to process.
    """


class NPMException(BaseCommonException):
    """Base exception for the NPM registry client"""


class NPMPackgeIntegrityError(NPMException):
    """Hash mismatch exception"""


class ResolverError(Exception):
    """
    The resolver class was not able to resolve the requested attribute.
    This is a not fatal exception and just makes the resolver pipeline
    try the next resolver class in the list.
    """


class ResolverPipelineError(Exception):
    """
    Raised when the resolver pipeline exhausted the list of resolvers
    and nothing new was returned. This means that the requested
    attribute does not exists.
    """
