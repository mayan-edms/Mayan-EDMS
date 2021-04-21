class ConvertError(Exception):
    """
    Base exception for all coverter app exceptions
    """


class AppImageError(ConvertError):
    """
    Exception to allow app specific error codes. These are errors that might
    need additional handling and that are not just a generic unknown format
    error.
    """
    def __init__(self, error_name):
        self.error_name = error_name
        super().__init__()

    def __str__(self):
        return('Error name: {}'.format(repr(self.error_name)))


class UnknownFileFormat(ConvertError):
    """
    Raised when the converter backend can't understand a file
    """


class UnkownConvertError(ConvertError):
    """
    Raised when an error is found but there is no disernible way to
    identify the kind of error
    """


class OfficeConversionError(ConvertError):
    """
    Used to encapsulate errors while executing Libre Office or when Libre
    Office is now available.
    """


class InvalidOfficeFormat(ConvertError):
    """
    Raised by the file type introspection code to signal that the file is not
    a office format file and that Libre Office will not be used to process
    it.
    """


class PageCountError(ConvertError):
    """
    Raised when an error is encountered while determining the page count of a
    file.
    """
