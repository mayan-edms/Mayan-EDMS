from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, ugettext

from solo.models import SingletonModel

from permissions.models import Role, StoredPermission

from .api import get_classes
from .classes import AccessObjectClass
from .managers import AccessEntryManager, DefaultAccessEntryManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class AccessEntry(models.Model):
    """
    Model that hold the permission, object, actor relationship
    """
    permission = models.ForeignKey(StoredPermission, verbose_name=_('Permission'))
    role = models.ForeignKey(Role, verbose_name=_('Role'))
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

    def __str__(self):
        return '%s: %s' % (self.content_type, self.content_object)
