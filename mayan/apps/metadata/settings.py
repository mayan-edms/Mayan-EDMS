from __future__ import unicode_literals

import yaml

from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace
from smart_settings.api import register_settings

from .parsers import MetadataParser

default_available_functions = {
    'current_date': now().date,
}

default_available_models = {
    'User': User
}

register_settings(
    namespace='metadata',
    module='metadata.settings',
    settings=[
        # Definition
        {'name': 'AVAILABLE_FUNCTIONS', 'global_name': 'METADATA_AVAILABLE_FUNCTIONS', 'default': default_available_functions},
        {'name': 'AVAILABLE_MODELS', 'global_name': 'METADATA_AVAILABLE_MODELS', 'default': default_available_models},
    ]
)

# TODO: remove classes, import by string, all settings must be simple serializable types

namespace = Namespace(name='metadata', label=_('Metadata'))
setting_available_validators = namespace.add_setting(global_name='METADATA_AVAILABLE_VALIDATORS', default=MetadataParser.get_import_paths())
