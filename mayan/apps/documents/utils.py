from __future__ import unicode_literals

import pycountry

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from .literals import DOCUMENT_IMAGES_CACHE_NAME


def callback_update_cache_size(setting):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    cache = Cache.objects.get(name=DOCUMENT_IMAGES_CACHE_NAME)
    cache.maximum_size = setting.value
    cache.save()


def get_language(language_code):
    language = getattr(
        pycountry.languages.get(alpha_3=language_code), 'name', None
    )

    if language:
        return _(language)
    else:
        return _('Unknown language "%s"') % language_code


def get_language_choices():
    from .settings import setting_language_codes

    return sorted(
        [
            (
                iso639_3, _(pycountry.languages.get(alpha_3=iso639_3).name)
            ) for iso639_3 in setting_language_codes.value
        ], key=lambda x: x[1]
    )


def parse_range(astr):
    # http://stackoverflow.com/questions/4248399/
    # page-range-for-printing-algorithm
    result = set()
    for part in astr.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return sorted(result)
