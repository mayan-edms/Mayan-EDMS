from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .parsers import MetadataParser
from .validators import MetadataValidator

namespace = SettingNamespace(label=_('Metadata'), name='metadata')

setting_available_validators = namespace.add_setting(
    global_name='METADATA_AVAILABLE_VALIDATORS',
    default=MetadataValidator.get_import_paths()
)
setting_available_parsers = namespace.add_setting(
    global_name='METADATA_AVAILABLE_PARSERS',
    default=MetadataParser.get_import_paths()
)
