from __future__ import unicode_literals

from datetime import timedelta
import logging

from django.utils.timezone import now

from mayan.celery import app

from .literals import UPLOAD_EXPIRATION_INTERVAL
from .models import SharedUploadedFile

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_delete_stale_uploads():
    logger.info('Executing')

    for expired_upload in SharedUploadedFile.objects.filter(datetime__lt=now() - timedelta(seconds=UPLOAD_EXPIRATION_INTERVAL)):
        expired_upload.delete()

    logger.info('Finshed')
