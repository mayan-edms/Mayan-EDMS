from __future__ import unicode_literals


class ParserError(Exception):
    """
    Base exception for file parsers
    """
    pass


class NoMIMETypeMatch(ParserError):
    """
    There is no parser registered for the specified MIME type
    """
    pass
