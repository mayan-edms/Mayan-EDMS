from __future__ import unicode_literals

import pycountry

from django.utils.translation import ugettext_lazy as _

from .settings import setting_language_codes

language_choices = sorted(
    [
        (
            iso639_3, _(pycountry.languages.get(alpha_3=iso639_3).name)
        ) for iso639_3 in setting_language_codes.value
    ], key=lambda x: x[1]
)
