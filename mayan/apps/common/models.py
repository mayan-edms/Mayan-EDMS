from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from solo.models import SingletonModel

from .managers import AnonymousUserSingletonManager
from .runtime import shared_storage_backend

SHARED_UPLOADED_FILE_PATH = 'shared_uploads'


def upload_to(instance, filename):
    instance.filename = filename
    return u'/'.join([SHARED_UPLOADED_FILE_PATH, filename])


class AnonymousUserSingleton(SingletonModel):
    objects = AnonymousUserSingletonManager()

    def __unicode__(self):
        return ugettext('Anonymous user')

    class Meta:
        verbose_name = verbose_name_plural = _(u'Anonymous user')


class AutoAdminSingleton(SingletonModel):
    account = models.ForeignKey(User, null=True, blank=True, related_name='auto_admin_account', verbose_name=_(u'Account'))
    password = models.CharField(null=True, blank=True, verbose_name=_(u'Password'), max_length=128)
    password_hash = models.CharField(null=True, blank=True, verbose_name=_(u'Password hash'), max_length=128)

    class Meta:
        verbose_name = verbose_name_plural = _(u'Auto admin properties')


class SharedUploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to, storage=shared_storage_backend, verbose_name=_(u'File'))
    filename = models.CharField(max_length=255, verbose_name=_('Filename'))
    datatime = models.DateTimeField(auto_now_add=True, verbose_name=_('Date time'))

    class Meta:
        verbose_name = _(u'Shared uploaded file')
        verbose_name_plural = _(u'Shared uploaded files')

    def __unicode__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.file.path)
        return super(SharedUploadedFile, self).delete(*args, **kwargs)
