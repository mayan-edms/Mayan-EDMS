import logging

from django.apps import apps

from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_download_files_stale_delete():
    logger.debug('Executing')

    DownloadFile = apps.get_model(
        app_label='storage', model_name='DownloadFile'
    )

    queryset = DownloadFile.objects.stale()

    logger.debug('Queryset count: %d', queryset.count())

    for expired_download in queryset.all():
        expired_download.delete()

    logger.debug('Finished')


@app.task(ignore_result=True)
def task_shared_upload_stale_delete():
    logger.debug('Executing')

    SharedUploadedFile = apps.get_model(
        app_label='storage', model_name='SharedUploadedFile'
    )

    queryset = SharedUploadedFile.objects.stale()

    logger.debug('Queryset count: %d', queryset.count())

    for expired_upload in queryset.all():
        expired_upload.delete()

    logger.debug('Finished')
