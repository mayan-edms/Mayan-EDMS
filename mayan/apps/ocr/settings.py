from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_OCR_AUTO_OCR, DEFAULT_OCR_BACKEND, DEFAULT_OCR_BACKEND_ARGUMENTS
)
from .setting_migrations import OCRSettingMigration

namespace = SettingNamespace(
    label=_('OCR'), migration_class=OCRSettingMigration, name='ocr',
    version='0003'
)

setting_auto_ocr = namespace.add_setting(
    default=DEFAULT_OCR_AUTO_OCR, global_name='OCR_AUTO_OCR', help_text=_(
        'Set new document types to perform OCR automatically by default.'
    )
)
setting_ocr_backend = namespace.add_setting(
    default=DEFAULT_OCR_BACKEND, global_name='OCR_BACKEND', help_text=_(
        'Full path to the backend to be used to do OCR.'
    )
)
setting_ocr_backend_arguments = namespace.add_setting(
    default=DEFAULT_OCR_BACKEND_ARGUMENTS,
    global_name='OCR_BACKEND_ARGUMENTS'
)
