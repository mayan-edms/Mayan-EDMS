import logging

from django.apps import apps
from django.contrib.auth import get_user_model

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(bind=True, ignore_result=True)
def task_cache_partition_purge(
    self, cache_partition_id, content_type_id=None, object_id=None,
    user_id=None
):
    CachePartition = apps.get_model(
        app_label='file_caching', model_name='CachePartition'
    )
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    User = get_user_model()

    cache_partition = CachePartition.objects.get(pk=cache_partition_id)

    if content_type_id and object_id:
        content_type = ContentType.objects.get(pk=content_type_id)
        content_object = content_type.get_object_for_this_type(pk=object_id)
    else:
        content_object = None

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    logger.info('Starting cache partition id %s purge', cache_partition)

    try:
        cache_partition._event_action_object = content_object
        cache_partition._event_actor = user
        cache_partition.purge()
    except LockError as exception:
        raise self.retry(exc=exception)
    else:
        logger.info('Finished cache partition id %s purge', cache_partition)


@app.task(bind=True, ignore_result=True)
def task_cache_purge(self, cache_id, user_id=None):
    Cache = apps.get_model(
        app_label='file_caching', model_name='Cache'
    )
    User = get_user_model()

    cache = Cache.objects.get(pk=cache_id)
    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    logger.info('Starting cache id %s purge', cache)
    try:
        cache._event_actor = user
        cache._event_keep_attributes = ('_event_actor',)
        cache.purge()
    except LockError as exception:
        raise self.retry(exc=exception)
    else:
        logger.info('Finished cache id %s purge', cache)
