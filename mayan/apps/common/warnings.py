from __future__ import absolute_import


class DatabaseWarning(UserWarning):
    """
    Warning when using unsupported database backends
    """


class InterfaceWarning(UserWarning):
    """
    Warning when using obsolete internal interfaces
    """
