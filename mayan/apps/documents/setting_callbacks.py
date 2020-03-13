from __future__ import unicode_literals

import logging

from django.apps import apps

from .literals import DOCUMENT_IMAGES_CACHE_NAME

logger = logging.getLogger(name=__name__)


def callback_update_cache_size(setting):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    cache = Cache.objects.get(name=DOCUMENT_IMAGES_CACHE_NAME)
    cache.maximum_size = setting.value
    cache.save()
