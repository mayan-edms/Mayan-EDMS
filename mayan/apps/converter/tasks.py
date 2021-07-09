import logging

from django.apps import apps
from django.contrib.auth import get_user_model

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(bind=True, retry_backoff=True)
def task_content_object_image_generate(
    self, content_type_id, object_id, user_id=None, **kwargs
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

    try:
        return obj.generate_image(user=user, **kwargs)
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate image for %s. Retrying.',
            obj
        )
        raise self.retry(exc=exception)
