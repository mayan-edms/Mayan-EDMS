from __future__ import unicode_literals

from pytz import common_timezones

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from .runtime import shared_storage_backend

SHARED_UPLOADED_FILE_PATH = 'shared_uploads'


def upload_to(instance, filename):
    instance.filename = filename
    return '/'.join([SHARED_UPLOADED_FILE_PATH, filename])


@python_2_unicode_compatible
class SharedUploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to, storage=shared_storage_backend, verbose_name=_('File'))
    filename = models.CharField(max_length=255, verbose_name=_('Filename'))
    datatime = models.DateTimeField(auto_now_add=True, verbose_name=_('Date time'))

    class Meta:
        verbose_name = _('Shared uploaded file')
        verbose_name_plural = _('Shared uploaded files')

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.path)
        return super(SharedUploadedFile, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class UserLocaleProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='locale_profile', verbose_name=_('User'))

    timezone = models.CharField(choices=zip(common_timezones, common_timezones), max_length=48, verbose_name=_('Timezone'))
    language = models.CharField(choices=settings.LANGUAGES, max_length=8, verbose_name=_('Language'))

    def __str__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _('User locale profile')
        verbose_name_plural = _('User locale profiles')
