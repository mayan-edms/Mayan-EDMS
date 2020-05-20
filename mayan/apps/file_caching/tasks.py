import logging

from django.apps import apps
from django.contrib.auth import get_user_model

from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_cache_purge(cache_id, user_id=None):
    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )
    User = get_user_model()

    cache = Cache.objects.get(pk=cache_id)
    user = User.objects.get(pk=user_id)

    logger.info('Starting cache id %s purge', cache)
    cache.purge(_user=user)
    logger.info('Finished cache id %s purge', cache)
