class ParserError(Exception):
    """
    Raised when a text parser fails to understand a file it been passed
    or the resulting parsed text is invalid
    """
    pass


class ParserUnknownFile(Exception):
    pass
