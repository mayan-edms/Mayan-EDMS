import logging

from django.apps import apps

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchRetry

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True
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
def task_index_search_model(self, search_model_full_name):
    search_model = SearchModel.get(name=search_model_full_name)

    for instance in search_model.model._meta.default_manager.all():
        task_index_instance.apply_async(
            kwargs={
                'app_label': instance._meta.app_label,
                'model_name': instance._meta.model_name,
                'object_id': instance.pk
            }
        )


@app.task(
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True
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
