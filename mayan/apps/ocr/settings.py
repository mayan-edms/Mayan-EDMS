from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .setting_migrations import OCRSettingMigration

namespace = SettingNamespace(
    label=_('OCR'), migration_class=OCRSettingMigration, name='ocr',
    version='0002'
)

setting_ocr_backend = namespace.add_setting(
    global_name='OCR_BACKEND',
    default='mayan.apps.ocr.backends.tesseract.Tesseract',
    help_text=_('Full path to the backend to be used to do OCR.')
)
setting_ocr_backend_arguments = namespace.add_setting(
    global_name='OCR_BACKEND_ARGUMENTS',
    default={}
)
setting_auto_ocr = namespace.add_setting(
    global_name='OCR_AUTO_OCR', default=True,
    help_text=_(
        'Set new document types to perform OCR automatically by default.'
    )
)
