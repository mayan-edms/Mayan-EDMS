import logging

from django.apps import apps

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchException, DynamicSearchRetry
from .literals import (
    TASK_DEINDEX_INSTANCE_MAX_RETRIES,
    TASK_DEINDEX_INSTANCE_RETRY_BACKOFF_MAX, TASK_INDEX_INSTANCE_MAX_RETRIES,
    TASK_INDEX_INSTANCE_RETRY_BACKOFF_MAX, TASK_INDEX_INSTANCES_MAX_RETRIES,
    TASK_INDEX_INSTANCES_RETRY_BACKOFF_MAX,
    TASK_INDEX_RELATED_INSTANCE_M2M_MAX_RETRIES,
    TASK_INDEX_RELATED_INSTANCE_M2M_RETRY_BACKOFF_MAX
)

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, ignore_result=True,
    max_retries=TASK_DEINDEX_INSTANCE_MAX_RETRIES, retry_backoff=True,
    retry_backoff_max=TASK_DEINDEX_INSTANCE_RETRY_BACKOFF_MAX
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
    max_retries=TASK_INDEX_INSTANCE_MAX_RETRIES, retry_backoff=True,
    retry_backoff_max=TASK_INDEX_INSTANCE_RETRY_BACKOFF_MAX
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
    max_retries=TASK_INDEX_INSTANCES_MAX_RETRIES, retry_backoff=True,
    retry_backoff_max=TASK_INDEX_INSTANCES_RETRY_BACKOFF_MAX
)
def task_index_instances(self, search_model_full_name, id_list):
    search_model = SearchModel.get(name=search_model_full_name)

    kwargs = {
        'id_list': id_list, 'search_model': search_model
    }

    try:
        SearchBackend.get_instance().index_instances(**kwargs)
    except (DynamicSearchRetry, LockError) as exception:
        raise self.retry(exc=exception)
    except Exception as exception:
        error_message = (
            'Unexpected error calling `task_index_instances` with '
            'keyword arguments {}.'
        ).format(kwargs)

        logger.error(error_message)
        raise DynamicSearchException(error_message) from exception


@app.task(
    bind=True, ignore_result=True,
    max_retries=TASK_INDEX_RELATED_INSTANCE_M2M_MAX_RETRIES,
    retry_backoff=True,
    retry_backoff_max=TASK_INDEX_RELATED_INSTANCE_M2M_RETRY_BACKOFF_MAX
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
        for id_list in search_model.get_id_groups():
            task_index_instances.apply_async(
                kwargs={
                    'id_list': id_list,
                    'search_model_full_name': search_model.get_full_name(),
                }
            )
