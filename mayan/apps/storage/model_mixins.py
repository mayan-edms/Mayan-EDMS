import logging

from django.core.files.base import ContentFile
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ugettext

logger = logging.getLogger(name=__name__)


class DatabaseFileModelMixin(models.Model):
    filename = models.CharField(
        db_index=True, max_length=255, verbose_name=_('Filename')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date time')
    )

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        name = self.file.name
        self.file.close()

        if name:
            self.file.storage.delete(name=name)
        return super().delete(*args, **kwargs)

    def open(self, **kwargs):
        default_kwargs = {
            'mode': self.file.file.mode,
            'name': self.file.name
        }

        # Close the self.file object as Django generates a new descriptor
        # when the file field is accessed.
        # From django/db/models/fields/files.py.
        """
        The descriptor for the file attribute on the model instance. Return a
        FieldFile when accessed so you can write code like::

            >>> from myapp.models import MyModel
            >>> instance = MyModel.objects.get(pk=1)
            >>> instance.file.size

        Assign a file object on assignment so you can do::

            >>> with open('/path/to/hello.world', 'r') as f:
            ...     instance.file = File(f)
        """
        self.file.close()
        self.file.file.close()

        default_kwargs.update(**kwargs)

        # Ensure the caller cannot specify an alternate filename.
        name = kwargs.pop('name', None)

        if name:
            logger.warning(
                'Caller tried to specify an alternate filename: %s', name
            )

        return self.file.storage.open(**default_kwargs)

    def save(self, *args, **kwargs):
        if not self.file:
            self.file = ContentFile(
                content='', name=self.filename or ugettext('Unnamed file')
            )

        self.filename = self.filename or force_text(s=self.file)
        super().save(*args, **kwargs)
