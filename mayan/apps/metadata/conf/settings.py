"""Configuration options for the metadata app"""

import datetime

from django.contrib.auth.models import User
from django.utils.timezone import now

from smart_settings.api import register_settings


default_available_functions = {
    'current_date': now().date,
}

default_available_models = {
    'User': User
}

register_settings(
    namespace=u'metadata',
    module=u'metadata.conf.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_FUNCTIONS', 'global_name': u'METADATA_AVAILABLE_FUNCTIONS', 'default': default_available_functions},
        {'name': u'AVAILABLE_MODELS', 'global_name': u'METADATA_AVAILABLE_MODELS', 'default': default_available_models},
    ]
)
