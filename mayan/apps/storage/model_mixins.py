from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ugettext


class DatabaseFileModelMixin(models.Model):
    filename = models.CharField(
        db_index=True, max_length=255, verbose_name=_('Filename')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date time')
    )

    def delete(self, *args, **kwargs):
        if self.file.name:
            self.file.storage.delete(name=self.file.name)
        return super().delete(*args, **kwargs)

    def open(self, mode=None):
        return self.file.storage.open(
            mode=mode or self.file.file.mode, name=self.file.name
        )

    def save(self, *args, **kwargs):
        if not self.file:
            self.file = ContentFile(
                content='', name=self.filename or ugettext('Unnamed file')
            )

        self.filename = self.filename or force_text(s=self.file)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
