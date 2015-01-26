from __future__ import unicode_literals

from dateutil.parser import parse

from django.contrib.auth.models import User
from django.utils.timezone import now

from smart_settings.api import register_settings

default_available_functions = {
    'current_date': now().date,
}

default_available_models = {
    'User': User
}

default_available_validators = {
    'Parse date and time': lambda input: parse(input).isoformat(),
    'Parse date': lambda input: parse(input).date().isoformat(),
    'Parse time': lambda input: parse(input).time().isoformat()
}

register_settings(
    namespace='metadata',
    module='metadata.settings',
    settings=[
        # Definition
        {'name': 'AVAILABLE_FUNCTIONS', 'global_name': 'METADATA_AVAILABLE_FUNCTIONS', 'default': default_available_functions},
        {'name': 'AVAILABLE_MODELS', 'global_name': 'METADATA_AVAILABLE_MODELS', 'default': default_available_models},
        {'name': 'AVAILABLE_VALIDATORS', 'global_name': 'METADATA_AVAILABLE_VALIDATORS', 'default': default_available_validators},
    ]
)
