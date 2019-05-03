from __future__ import unicode_literals


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


class CompressionFileError(BaseCommonException):
    """
    Base exception for file decompression class
    """
    pass


class NoMIMETypeMatch(CompressionFileError):
    """
    There is no decompressor registered for the specified MIME type
    """
    pass


class NPMException(BaseCommonException):
    """Base exception for the NPM registry client"""


class NPMPackgeIntegrityError(NPMException):
    """Hash mismatch exception"""
