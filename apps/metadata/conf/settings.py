"""Configuration options for the metadata app"""

import datetime

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

default_available_functions = {
    'current_date': datetime.datetime.now().date,
}

default_available_models = {
    'User': User
}

namespace = SettingNamespace('metadata', _(u'Metadata'), module='metadata.conf.settings')

Setting(
    namespace=namespace,
    name=u'AVAILABLE_FUNCTIONS',
    global_name=u'METADATA_AVAILABLE_FUNCTIONS',
    default=default_available_functions,
)

Setting(
    namespace=namespace,
    name=u'AVAILABLE_MODELS',
    global_name=u'METADATA_AVAILABLE_MODELS',
    default=default_available_models,
)
