from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_METADATA_AVAILABLE_PARSERS, DEFAULT_METADATA_AVAILABLE_VALIDATORS
)

namespace = SettingNamespace(label=_('Metadata'), name='metadata')

setting_available_parsers = namespace.add_setting(
    default=DEFAULT_METADATA_AVAILABLE_PARSERS,
    global_name='METADATA_AVAILABLE_PARSERS'
)
setting_available_validators = namespace.add_setting(
    default=DEFAULT_METADATA_AVAILABLE_VALIDATORS,
    global_name='METADATA_AVAILABLE_VALIDATORS'
)
