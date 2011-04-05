class ConvertError(Exception):
    '''Base exception for all coverter app exceptions
    '''
    pass


class UnknownFormat(ConvertError):
    '''Raised when the converter backend can't understand or there
    isn't an appropiate driver available'''
    pass


class UnpaperError(ConvertError):
    '''Raised by upaper
    '''
    pass
    
    
class IdentifyError(ConvertError):
    '''Raised by identify
    '''
    pass

    
class UnkownConvertError(ConvertError):
    '''Raised when an error is found but there is no disernible way to 
    identify the kind of error
    '''
    pass
