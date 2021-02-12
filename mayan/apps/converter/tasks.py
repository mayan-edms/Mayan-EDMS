import logging

from django.apps import apps

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .literals import TASK_ASSET_IMAGE_GENERATE_RETRY_DELAY

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, default_retry_delay=TASK_ASSET_IMAGE_GENERATE_RETRY_DELAY
)
def task_asset_image_generate(self, asset_id):
    Asset = apps.get_model(
        app_label='converter', model_name='Asset'
    )

    asset = Asset.objects.get(pk=asset_id)

    try:
        return asset.generate_image()
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate asset "%s" image. '
            'Retrying.', asset.internal_name
        )
        raise self.retry(exc=exception)
