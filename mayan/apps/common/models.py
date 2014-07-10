from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import User

from solo.models import SingletonModel

from .managers import AnonymousUserSingletonManager


class AnonymousUserSingleton(SingletonModel):
    objects = AnonymousUserSingletonManager()

    def __unicode__(self):
        return ugettext('Anonymous user')

    class Meta:
        verbose_name = _(u'anonymous user')
        verbose_name_plural = _(u'anonymous user')


class AutoAdminSingleton(SingletonModel):
    account = models.ForeignKey(User, null=True, blank=True, related_name='auto_admin_account', verbose_name=_(u'account'))
    password = models.CharField(null=True, blank=True, verbose_name=_(u'password'), max_length=128)
    password_hash = models.CharField(null=True, blank=True, verbose_name=_(u'password hash'), max_length=128)

    class Meta:
        verbose_name = verbose_name_plural = _(u'auto admin properties')
