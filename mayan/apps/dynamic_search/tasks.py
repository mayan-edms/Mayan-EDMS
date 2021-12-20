import logging

from django.apps import apps
from django.db.models.aggregates import Max, Min

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchException, DynamicSearchRetry
from .literals import (
    TASK_DEINDEX_INSTANCE_MAX_RETRIES, TASK_INDEX_INSTANCE_MAX_RETRIES
)
from .settings import setting_indexing_chunk_size

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, ignore_result=True,
    max_retries=TASK_DEINDEX_INSTANCE_MAX_RETRIES, retry_backoff=True
)
def task_deindex_instance(self, app_label, model_name, object_id):
    logger.info('Executing')

    Model = apps.get_model(app_label=app_label, model_name=model_name)
    instance = Model._meta.default_manager.get(pk=object_id)

    try:
        SearchBackend.get_instance().deindex_instance(instance=instance)
    except (DynamicSearchRetry, LockError) as exception:
        raise self.retry(exc=exception)

    logger.info('Finished')


@app.task(
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True
)
def task_index_search_model(self, search_model_full_name, range_string=None):
    search_model = SearchModel.get(name=search_model_full_name)

    kwargs = {
        'range_string': range_string, 'search_model': search_model
    }

    try:
        SearchBackend.get_instance().index_search_model(**kwargs)
    except Exception as exception:
        raise DynamicSearchException(
            'Unexpected error calling `index_search_model` with '
            'keyword arguments {}.'.format(kwargs)
        ) from exception


@app.task(
    bind=True, ignore_result=True,
    max_retries=TASK_INDEX_INSTANCE_MAX_RETRIES, retry_backoff=True
)
def task_index_instance(
    self, app_label, model_name, object_id, exclude_app_label=None,
    exclude_model_name=None, exclude_kwargs=None
):
    logger.info('Executing')

    Model = apps.get_model(app_label=app_label, model_name=model_name)
    if exclude_app_label and exclude_model_name:
        ExcludeModel = apps.get_model(
            app_label=exclude_app_label, model_name=exclude_model_name
        )
    else:
        ExcludeModel = None

    instance = Model._meta.default_manager.get(pk=object_id)

    try:
        SearchBackend.get_instance().index_instance(
            instance=instance, exclude_model=ExcludeModel,
            exclude_kwargs=exclude_kwargs
        )
    except (DynamicSearchRetry, LockError) as exception:
        raise self.retry(exc=exception)

    logger.info('Finished')


@app.task(ignore_result=True)
def task_reindex_backend():
    backend = SearchBackend.get_instance()
    backend.reset()

    for search_model in SearchModel.all():
        queryset = search_model.model._meta.managers_map[search_model.manager_name].all()
        if queryset:
            queryset = queryset.aggregate(min_id=Min('id'), max_id=Max('id'))
            step = setting_indexing_chunk_size.value - 1

            for id_start in range(queryset['min_id'], queryset['max_id'] + 1, step):
                range_string = '{}-{}'.format(id_start, id_start + step - 1)
                task_index_search_model.apply_async(
                    kwargs={
                        'range_string': range_string,
                        'search_model_full_name': search_model.get_full_name(),
                    }
                )
