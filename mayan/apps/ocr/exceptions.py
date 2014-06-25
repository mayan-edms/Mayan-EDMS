class AlreadyQueued(Exception):
    """
    Raised when a trying to queue document already in the queue
    """
    pass


class OCRError(Exception):
    """
    Raised by the OCR backend
    """
    pass


class UnpaperError(Exception):
    """
    Raised by unpaper
    """
    pass


class ReQueueError(Exception):
    pass
