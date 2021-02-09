from mayan.apps.smart_settings.classes import SettingNamespaceMigration
from mayan.apps.smart_settings.utils import smart_yaml_load


class OCRSettingMigration(SettingNamespaceMigration):
    def ocr_backend_0002(self, value):
        """
        The PyOCR backed was removed in version 3.5, this migration
        switches the backend to the Tesseract one.
        """
        return 'mayan.apps.ocr.backends.tesseract.Tesseract'

    def ocr_backend_arguments_0001(self, value):
        """
        From version 0001 to 0002 backend arguments are no longer quoted
        but YAML valid too. Changed in version 3.3.
        """
        return smart_yaml_load(value=value)
