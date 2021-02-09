class CompressionFileError(Exception):
    """
    Base exception for file decompression class
    """


class NoMIMETypeMatch(CompressionFileError):
    """
    There is no decompressor registered for the specified MIME type
    """
