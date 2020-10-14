from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from .literals import (
    INTERVAL_DOWNLOAD_FILE_EXPIRATION, INTERVAL_SHARED_UPLOAD_STALE
)


class DownloadFileManager(models.Manager):
    def stale(self):
        return self.filter(
            datetime__lt=now() - timedelta(
                seconds=INTERVAL_DOWNLOAD_FILE_EXPIRATION
            )
        )


class SharedUploadedFileManager(models.Manager):
    def stale(self):
        return self.filter(
            datetime__lt=now() - timedelta(
                seconds=INTERVAL_SHARED_UPLOAD_STALE
            )
        )
