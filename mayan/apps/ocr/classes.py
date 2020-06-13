from django.utils.module_loading import import_string

from mayan.apps.converter.classes import ConverterBase

from .settings import setting_ocr_backend, setting_ocr_backend_arguments


class OCRBackendBase:
    @staticmethod
    def get_instance():
        return import_string(
            dotted_path=setting_ocr_backend.value
        )(**setting_ocr_backend_arguments.value)

    def execute(self, file_object, language=None, transformations=None):
        self.language = language

        if not transformations:
            transformations = []

        self.converter = ConverterBase.get_converter_class()(
            file_object=file_object
        )

        for transformation in transformations:
            self.converter.transform(transformation=transformation)
