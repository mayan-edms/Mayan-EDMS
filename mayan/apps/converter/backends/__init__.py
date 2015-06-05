from __future__ import unicode_literals


class ConverterBase(object):
    """
    Base class that all backend classes must inherit
    """

    def convert(self, input_data, ):
        raise NotImplementedError()

    def transform(self, input_data, transformations):
        raise NotImplementedError()

    def get_page_count(self, input_data):
        raise NotImplementedError()
