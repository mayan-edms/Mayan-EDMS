class ConverterBase(object):
    """
    Base class that all backend classes must inherit
    """
    def convert_file(self, input_filepath, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a convert_file() method, which is required." % self.__class__.__name__)

    def convert_document(self, document, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a convert_document() method, which is required." % self.__class__.__name__)

    def get_format_list(self):
        raise NotImplementedError("Your %s class has not defined a get_format_list() method, which is required." % self.__class__.__name__)

    def get_available_transformations(self):
        raise NotImplementedError("Your %s class has not defined a get_available_transformations() method, which is required." % self.__class__.__name__)

    def get_page_count(self):
        raise NotImplementedError("Your %s class has not defined a get_page_count() method, which is required." % self.__class__.__name__)
