from __future__ import unicode_literals

import logging

import pycountry

from django.utils.translation import ugettext_lazy as _

from .settings import setting_language_codes

logger = logging.getLogger(name=__name__)


def get_language(language_code):
    language = getattr(
        pycountry.languages.get(alpha_3=language_code), 'name', None
    )

    if language:
        return _(language)
    else:
        return _('Unknown language "%s"') % language_code


def get_language_choices():
    result = []

    for iso639_3 in setting_language_codes.value:
        entry = pycountry.languages.get(alpha_3=iso639_3)
        if entry:
            label = _(entry.name)
            result.append(
                (iso639_3, label)
            )
        else:
            logger.warning('Unknown language code "%s".', iso639_3)

    return sorted(result, key=lambda x: x[1])


def parse_range(astr):
    # http://stackoverflow.com/questions/4248399/
    # page-range-for-printing-algorithm
    result = set()
    for part in astr.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(result)
