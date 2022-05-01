from django.db import models

from .events import event_error_log_deleted


class ErrorLogPartitionEntryManager(models.Manager):
    def clear(self, _user=None):
        content_object = self.instance.content_object
        self.all().delete()

        event_error_log_deleted.commit(actor=_user, target=content_object)
