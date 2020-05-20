from ..classes import OCRBackendBase


class NoOpOCR(OCRBackendBase):
    def __init__(self, *args, **kwargs):
        super(NoOpOCR, self).__init__(*args, **kwargs)

    def execute(self, *args, **kwargs):
        """Don't do anything"""
