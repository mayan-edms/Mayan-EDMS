class AlreadyQueued(Exception):
    """
    Raised when a trying to queue document already in the queue
    """
    pass


class TesseractError(Exception):
    """
    Raised by tesseract
    """
    pass


class UnpaperError(Exception):
    """
    Raised by unpaper
    """
    pass


class ReQueueError(Exception):
    pass


class OCRProcessingAlreadyDisabled(Exception):
    pass
    
    
class OCRProcessingAlreadyEnabled(Exception):
    pass
