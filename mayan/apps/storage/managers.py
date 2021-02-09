from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from mayan.apps.events.classes import EventModelRegistry, ModelEventType

from .events import (
    event_download_file_created, event_download_file_deleted
)
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

    def register_content_object(self, model):
        EventModelRegistry.register(model=model)

        ModelEventType.register(
            model=model, event_types=(
                event_download_file_created, event_download_file_deleted
            )
        )


class SharedUploadedFileManager(models.Manager):
    def stale(self):
        return self.filter(
            datetime__lt=now() - timedelta(
                seconds=INTERVAL_SHARED_UPLOAD_STALE
            )
        )
