class ConvertError(Exception):
    pass


class UnknownFormat(ConvertError):
    pass


class UnpaperError(ConvertError):
    pass
    
    
class IdentifyError(ConvertError):
    pass

    
class UnkownConvertError(ConvertError):
    pass
