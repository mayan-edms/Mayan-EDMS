from datetime import timedelta
import logging

from django.apps import apps
from django.utils.timezone import now

from mayan.celery import app

from .literals import UPLOAD_EXPIRATION_INTERVAL

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_delete_stale_uploads():
    logger.info('Executing')

    SharedUploadedFile = apps.get_model(
        app_label='storage', model_name='SharedUploadedFile'
    )

    queryset = SharedUploadedFile.objects.filter(
        datetime__lt=now() - timedelta(seconds=UPLOAD_EXPIRATION_INTERVAL)
    )

    for expired_upload in queryset:
        expired_upload.delete()

    logger.info('Finshed')
