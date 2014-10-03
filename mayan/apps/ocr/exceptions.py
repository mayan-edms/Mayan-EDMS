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
