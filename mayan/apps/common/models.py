from __future__ import unicode_literals

import uuid

from pytz import common_timezones

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .runtime import shared_storage_backend


def upload_to(instance, filename):
    return 'shared-file-{}'.format(uuid.uuid4().hex)


@python_2_unicode_compatible
class SharedUploadedFile(models.Model):
    file = models.FileField(
        storage=shared_storage_backend, upload_to=upload_to,
        verbose_name=_('File')
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

    def save(self, *args, **kwargs):
        self.filename = unicode(self.file)
        super(SharedUploadedFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.name)
        return super(SharedUploadedFile, self).delete(*args, **kwargs)

    def open(self):
        return self.file.storage.open(self.file.name)


@python_2_unicode_compatible
class UserLocaleProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='locale_profile',
        verbose_name=_('User')
    )
    timezone = models.CharField(
        choices=zip(common_timezones, common_timezones), max_length=48,
        verbose_name=_('Timezone')
    )
    language = models.CharField(
        choices=settings.LANGUAGES, max_length=8, verbose_name=_('Language')
    )

    def __str__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _('User locale profile')
        verbose_name_plural = _('User locale profiles')
