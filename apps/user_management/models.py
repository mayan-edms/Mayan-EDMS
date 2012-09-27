from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from common.models import Singleton


class AutoAdminSingleton(Singleton):
    account = models.ForeignKey(User, null=True, blank=True, related_name='auto_admin_account', verbose_name=_(u'account'))
    password = models.CharField(null=True, blank=True, verbose_name=_(u'password'), max_length=128)
    password_hash = models.CharField(null=True, blank=True, verbose_name=_(u'password hash'), max_length=128)

    class Meta:
        verbose_name = verbose_name_plural = _(u'auto admin properties')
