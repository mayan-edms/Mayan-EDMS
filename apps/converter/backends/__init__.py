class ConverterBase(object):
    """
    Base class that all backend classes must inherit
    """

    def identify_file(self, input_filepath, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a identify_file() method, which is required." % self.__class__.__name__)

    def identify_document(self, document, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a identify_document() method, which is required." % self.__class__.__name__)
    
    def convert_file(self, input_filepath, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a convert_file() method, which is required." % self.__class__.__name__)

    def convert_document(self, document, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a convert_document() method, which is required." % self.__class__.__name__)

    def get_format_list(self):
        raise NotImplementedError("Your %s class has not defined a get_format_list() method, which is required." % self.__class__.__name__)

    def get_available_transformations(self):
        raise NotImplementedError("Your %s class has not defined a get_available_transformations() method, which is required." % self.__class__.__name__)

    def get_available_transformations_labels(self):
        return ([(name, data['label']) for name, data in self.get_available_transformations().items()])

    def get_transformation_string(self, transformation_list):
        transformations = []
        warnings = []
        transformation_choices = self.get_available_transformations()
        for transformation in transformation_list:
            try:
                if transformation['transformation'] in transformation_choices:
                    transformations.append(
                        transformation_choices[transformation['transformation']]['command_line'] % eval(
                            transformation['arguments']
                        )
                    )
            except Exception, e:
                warnings.append(e)

        return u' '.join(transformations), warnings        
    
