from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

from .validators import MetadataValidator

default_available_functions = {
    'current_date': now().date,
}

default_available_models = {
    'User': User
}

namespace = Namespace(name='metadata', label=_('Metadata'))
setting_available_validators = namespace.add_setting(global_name='METADATA_AVAILABLE_VALIDATORS', default=MetadataValidator.get_import_paths())
setting_available_functions = namespace.add_setting(global_name='METADATA_AVAILABLE_FUNCTIONS', default=default_available_functions)
setting_available_models = namespace.add_setting(global_name='METADATA_AVAILABLE_MODELS', default=default_available_models)
