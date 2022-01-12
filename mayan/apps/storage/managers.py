from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from mayan.apps.events.classes import EventModelRegistry, ModelEventType

from .events import (
    event_download_file_created, event_download_file_deleted
)
from .settings import (
    setting_download_file_expiration_interval,
    setting_shared_uploaded_file_expiration_interval
)


class DownloadFileManager(models.Manager):
    def stale(self):
        return self.filter(
            datetime__lt=now() - timedelta(
                seconds=setting_download_file_expiration_interval.value
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
                seconds=setting_shared_uploaded_file_expiration_interval.value
            )
        )
