from __future__ import unicode_literals

#from importlib import import_module
#import logging
import os

#import yaml

from django.apps import apps
from django.conf import settings
#from django.utils.functional import Promise
#from django.utils.encoding import force_text, python_2_unicode_compatible

#SETTING_FILE_LAST_KNOWN_GOOD =
CONFIGURATION_FILENAME = '_settings.yml'
CONFIGURATION_FILEPATH = os.path.join(
    settings.MEDIA_ROOT, CONFIGURATION_FILENAME
)
