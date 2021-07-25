class BaseCommonException(Exception):
    """
    Base exception for the common app.
    """


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


class NonUniqueError(BaseCommonException):
    """
    Raised when attempting to add duplicate values to a type that expects
    them to be unique.
    """
