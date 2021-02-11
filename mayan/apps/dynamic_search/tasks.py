import logging

from django.apps import apps

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .classes import SearchBackend, SearchModel
from .literals import TASK_RETRY_DELAY

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, default_retry_delay=TASK_RETRY_DELAY, max_retries=None,
    ignore_result=True
)
def task_deindex_instance(self, app_label, model_name, object_id):
    logger.info('Executing')

    Model = apps.get_model(app_label=app_label, model_name=model_name)
    instance = Model._meta.default_manager.get(pk=object_id)

    try:
        SearchBackend.get_instance().deindex_instance(instance=instance)
    except LockError as exception:
        raise self.retry(exc=exception)

    logger.info('Finished')


@app.task(
    bind=True, default_retry_delay=TASK_RETRY_DELAY, max_retries=None,
    ignore_result=True
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
    bind=True, default_retry_delay=TASK_RETRY_DELAY, max_retries=None,
    ignore_result=True
)
def task_index_instance(self, app_label, model_name, object_id):
    logger.info('Executing')

    try:
        Model = apps.get_model(app_label=app_label, model_name=model_name)
    except LookupError:
        """
        The app or model does not exists anymore. Non fatal, just exit
        the task.
        """
    else:
        try:
            instance = Model._meta.default_manager.get(pk=object_id)
        except Model.DoesNotExist:
            """
            This is not fatal, the task is triggered on the post_save
            signal and the instance might still not be ready to access.
            """
        else:
            try:
                SearchBackend.get_instance().index_instance(instance=instance)
            except LockError as exception:
                raise self.retry(exc=exception)

    logger.info('Finished')
