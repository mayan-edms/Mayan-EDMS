import logging

import celery

from django.apps import apps
from django.contrib.auth import get_user_model

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .settings import setting_image_generation_max_retries
from .utils import IndexedDictionary

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, max_retries=setting_image_generation_max_retries.value,
    retry_backoff=True
)
def task_content_object_image_generate(
    self, content_type_id, object_id, maximum_layer_order=None,
    transformation_dictionary_list=None, user_id=None
):
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    User = get_user_model()

    content_type = ContentType.objects.get(pk=content_type_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    obj = content_type.get_object_for_this_type(pk=object_id)

    transformation_indexed_dictionary = IndexedDictionary.from_dictionary_list(
        dictionary_list=transformation_dictionary_list or ()
    )

    transformation_instance_list = transformation_indexed_dictionary.as_instance_list()

    try:
        return obj.generate_image(
            maximum_layer_order=maximum_layer_order,
            transformation_instance_list=transformation_instance_list,
            user=user
        )
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate image for %s. Retrying.',
            obj
        )
        try:
            raise self.retry(exc=exception)
        except celery.exceptions.MaxRetriesExceededError:
            logger.error(
                'Maximum retries reached for image generation task. '
                'System might be overloaded or a stale lock might be '
                'preventing the task from completing.'
            )
            raise
