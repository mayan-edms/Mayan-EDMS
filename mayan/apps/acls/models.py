from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from solo.models import SingletonModel

from permissions.models import StoredPermission

from .api import get_classes
from .classes import AccessObjectClass
from .managers import AccessEntryManager, DefaultAccessEntryManager

logger = logging.getLogger(__name__)


class AccessEntry(models.Model):
    """
    Model that hold the permission, object, actor relationship
    """
    permission = models.ForeignKey(StoredPermission, verbose_name=_('Permission'))

    holder_type = models.ForeignKey(
        ContentType,
        related_name='access_holder',
        limit_choices_to={'model__in': ('user', 'group', 'role')}
    )
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(
        ct_field='holder_type',
        fk_field='holder_id'
    )

    content_type = models.ForeignKey(
        ContentType,
        related_name='object_content_type'
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )

    objects = AccessEntryManager()

    class Meta:
        verbose_name = _('Access entry')
        verbose_name_plural = _('Access entries')

    def __unicode__(self):
        return '%s: %s' % (self.content_type, self.content_object)


class DefaultAccessEntry(models.Model):
    """
    Model that holds the permission, class, actor relationship, that will
    be added upon the creation of an instance of said class
    """
    @classmethod
    def get_classes(cls):
        return [AccessObjectClass.encapsulate(cls) for cls in get_classes()]

    permission = models.ForeignKey(StoredPermission, verbose_name=_('Permission'))

    holder_type = models.ForeignKey(
        ContentType,
        limit_choices_to={'model__in': ('user', 'group', 'role')},
        related_name='default_access_entry_holder'
    )
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(
        ct_field='holder_type',
        fk_field='holder_id'
    )

    content_type = models.ForeignKey(
        ContentType,
        related_name='default_access_entry_class'
    )

    objects = DefaultAccessEntryManager()

    class Meta:
        verbose_name = _('Default access entry')
        verbose_name_plural = _('Default access entries')

    def __unicode__(self):
        return '%s: %s' % (self.content_type, self.content_object)


class CreatorSingletonManager(models.Manager):
    def passthru_check(self, holder, creator=None):
        if isinstance(holder, self.model):
            # TODO: raise explicit error if is instance and creator=None
            return creator
        else:
            return holder


class CreatorSingleton(SingletonModel):
    objects = CreatorSingletonManager()

    def __unicode__(self):
        return ugettext('Creator')

    class Meta:
        verbose_name = _('Creator')
        verbose_name_plural = _('Creator')
