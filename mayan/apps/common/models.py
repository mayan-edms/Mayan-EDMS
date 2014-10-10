from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from solo.models import SingletonModel

from .managers import AnonymousUserSingletonManager


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
