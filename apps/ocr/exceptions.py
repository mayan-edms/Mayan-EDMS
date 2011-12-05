class AlreadyQueued(Exception):
    pass


class TesseractError(Exception):
    pass


class UnpaperError(Exception):
    """
    Raised by unpaper
    """
    pass


class ReQueueError(Exception):
    pass
