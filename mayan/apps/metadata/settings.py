"""Configuration options for the metadata app"""

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
    'parse_date': lambda input: parse(input).isoformat()
}

register_settings(
    namespace=u'metadata',
    module=u'metadata.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_FUNCTIONS', 'global_name': u'METADATA_AVAILABLE_FUNCTIONS', 'default': default_available_functions},
        {'name': u'AVAILABLE_MODELS', 'global_name': u'METADATA_AVAILABLE_MODELS', 'default': default_available_models},
        {'name': u'AVAILABLE_VALIDATORS', 'global_name': u'METADATA_AVAILABLE_VALIDATORS', 'default': default_available_validators},
    ]
)
