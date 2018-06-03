from __future__ import unicode_literals

#import os

import pycountry

#from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .settings import setting_language_codes

language_choices = [
    (
        iso639_3, _(pycountry.languages.get(alpha_3=iso639_3).name)
    ) for iso639_3 in setting_language_codes.value
]
