from pathlib import Path
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerMethodAfter, EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.permissions.models import StoredPermission

from .classes import DefinedStorageLazy
from .events import (
    event_download_file_created, event_download_file_deleted,
    event_download_file_downloaded
)
from .literals import (
    STORAGE_NAME_DOWNLOAD_FILE, STORAGE_NAME_SHARED_UPLOADED_FILE
)
from .managers import DownloadFileManager, SharedUploadedFileManager
from .model_mixins import DatabaseFileModelMixin


def download_file_upload_to(instance, filename):
    return 'download-file-{}'.format(uuid.uuid4().hex)


def upload_to(instance, filename):
    return 'shared-file-{}'.format(uuid.uuid4().hex)


class DownloadFile(DatabaseFileModelMixin, ExtraDataModelMixin, models.Model):
    """
    Keep a database link to a stored file. Used for generates files meant
    to be downloaded at a later time.
    """
    file = models.FileField(
        storage=DefinedStorageLazy(
            name=STORAGE_NAME_DOWNLOAD_FILE
        ), upload_to=download_file_upload_to, verbose_name=_('File')
    )
    content_type = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to=ContentType
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id'
    )
    label = models.CharField(
        db_index=True, max_length=192, verbose_name=_('Label')
    )
    permission = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        to=StoredPermission, verbose_name=_('Permission')
    )

    objects = DownloadFileManager()

    class Meta:
        ordering = ('-datetime',)
        verbose_name = _('Download file')
        verbose_name_plural = _('Download files')

    def __str__(self):
        if self.content_object:
            return str(self.content_object)
        else:
            return self.filename or self.label

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_download_file_deleted,
        target='content_object'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def get_absolute_url(self):
        if self.content_object:
            return self.content_object.get_absolute_url()

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_download_file_downloaded,
        target='self'
    )
    def get_download_file_object(self):
        return self.open(mode='rb')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'content_object',
            'event': event_download_file_created,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SharedUploadedFile(DatabaseFileModelMixin, models.Model):
    """
    Keep a database link to a stored file. Used to share files between code
    that runs out of process.
    """
    file = models.FileField(
        storage=DefinedStorageLazy(
            name=STORAGE_NAME_SHARED_UPLOADED_FILE
        ), upload_to=upload_to, verbose_name=_('File')
    )
    filename = models.CharField(
        blank=True, max_length=255, verbose_name=_('Filename')
    )

    objects = SharedUploadedFileManager()

    class Meta:
        verbose_name = _('Shared uploaded file')
        verbose_name_plural = _('Shared uploaded files')

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        self.filename = self.filename or Path(path=self.file.name).name
        super().save(*args, **kwargs)
