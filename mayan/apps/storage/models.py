import uuid

from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .classes import DefinedStorageLazy
from .literals import STORAGE_NAME_SHARED_UPLOADED_FILE


def upload_to(instance, filename):
    return 'shared-file-{}'.format(uuid.uuid4().hex)


class SharedUploadedFile(models.Model):
    """
    Keep a database link to a stored file. Used to share files between code
    that runs out of process.
    """
    file = models.FileField(
        storage=DefinedStorageLazy(
            name=STORAGE_NAME_SHARED_UPLOADED_FILE
        ), upload_to=upload_to, verbose_name=_('File')
    )
    filename = models.CharField(max_length=255, verbose_name=_('Filename'))
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date time')
    )

    class Meta:
        verbose_name = _('Shared uploaded file')
        verbose_name_plural = _('Shared uploaded files')

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.file.storage.delete(name=self.file.name)
        return super(SharedUploadedFile, self).delete(*args, **kwargs)

    def open(self):
        return self.file.storage.open(name=self.file.name)

    def save(self, *args, **kwargs):
        self.filename = force_text(self.file)
        super(SharedUploadedFile, self).save(*args, **kwargs)
