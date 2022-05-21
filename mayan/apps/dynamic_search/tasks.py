import logging

from django.apps import apps
from django.db.models.aggregates import Max, Min

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchException, DynamicSearchRetry
from .literals import (
    TASK_DEINDEX_INSTANCE_MAX_RETRIES, TASK_INDEX_INSTANCE_MAX_RETRIES,
    TASK_INDEX_RELATED_INSTANCE_M2M_MAX_RETRIES,
    TASK_INDEX_SEARCH_MODEL_MAX_RETRIES
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
    bind=True, ignore_result=True,
    max_retries=TASK_INDEX_SEARCH_MODEL_MAX_RETRIES, retry_backoff=True
)
def task_index_search_model(self, search_model_full_name, range_string=None):
    search_model = SearchModel.get(name=search_model_full_name)

    kwargs = {
        'range_string': range_string, 'search_model': search_model
    }

    try:
        SearchBackend.get_instance().index_search_model(**kwargs)
    except (DynamicSearchRetry, LockError) as exception:
        raise self.retry(exc=exception)
    except Exception as exception:
        error_message = (
            'Unexpected error calling `task_index_search_model` with '
            'keyword arguments {}.'
        ).format(kwargs)

        logger.error(error_message)
        raise DynamicSearchException(error_message) from exception


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

    try:
        instance = Model._meta.default_manager.get(pk=object_id)
    except Model.DoesNotExist as exception:
        raise self.retry(exc=exception)

    try:
        SearchBackend.get_instance().index_instance(
            instance=instance, exclude_model=ExcludeModel,
            exclude_kwargs=exclude_kwargs
        )
    except (DynamicSearchRetry, LockError) as exception:
        raise self.retry(exc=exception)
    except Exception as exception:
        kwargs = {
            'app_label': app_label,
            'model_name': model_name,
            'object_id': object_id,
            'exclude_app_label': exclude_app_label,
            'exclude_model_name': exclude_model_name,
            'exclude_kwargs': exclude_kwargs
        }
        error_message = (
            'Unexpected error calling `task_index_instance` with keyword '
            'arguments {}.'
        ).format(kwargs)

        logger.error(error_message)
        raise DynamicSearchException(error_message) from exception
    else:
        logger.info('Finished')


@app.task(
    bind=True, ignore_result=True,
    max_retries=TASK_INDEX_RELATED_INSTANCE_M2M_MAX_RETRIES,
    retry_backoff=True
)
def task_index_related_instance_m2m(
    self, action, instance_app_label, instance_model_name,
    instance_object_id, model_app_label, model_model_name, pk_set,
    serialized_search_model_related_paths
):
    InstanceModel = apps.get_model(
        app_label=instance_app_label, model_name=instance_model_name
    )
    instance = InstanceModel.objects.get(pk=instance_object_id)

    Model = apps.get_model(
        app_label=model_app_label, model_name=model_model_name
    )

    search_model_related_paths = {}

    for key, value in serialized_search_model_related_paths.items():
        app_label, model_name = key.split('.')
        DeserializedModel = apps.get_model(
            app_label=app_label, model_name=model_name
        )
        search_model_related_paths[DeserializedModel] = value

    SearchBackend.index_related_instance_m2m(
        action=action, instance=instance, model=Model, pk_set=pk_set,
        search_model_related_paths=search_model_related_paths
    )


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
