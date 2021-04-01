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
    pass


class UnkownConvertError(ConvertError):
    """
    Raised when an error is found but there is no disernible way to
    identify the kind of error
    """
    pass


class OfficeConversionError(ConvertError):
    pass


class InvalidOfficeFormat(ConvertError):
    pass


class PageCountError(ConvertError):
    pass

