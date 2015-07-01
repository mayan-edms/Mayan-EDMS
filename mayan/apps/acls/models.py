from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from permissions.models import Role, StoredPermission

from .managers import AccessControlListManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class AccessControlList(models.Model):
    """
    Model that hold the permission, object, actor relationship
    """

    content_type = models.ForeignKey(
        ContentType,
        related_name='object_content_type'
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id',
    )
    # TODO: limit choices to the permissions valid for the content_object
    permissions = models.ManyToManyField(StoredPermission, blank=True, related_name='acls', verbose_name=_('Permissions'))
    role = models.ForeignKey(Role, related_name='acls', verbose_name=_('Role'))

    objects = AccessControlListManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'role')
        verbose_name = _('Access entry')
        verbose_name_plural = _('Access entries')

    def __str__(self):
        return '{} <=> {}'.format(self.content_object, self.role)

'''
# TODO: remove
@python_2_unicode_compatible
class AccessControlList(models.Model):
    """
    Model that hold the permission, object, actor relationship
    """
    permission = models.ForeignKey(StoredPermission, verbose_name=_('Permission'))
    role = models.ForeignKey(Role, verbose_name=_('Role'))
    content_type = models.ForeignKey(
        ContentType,
        related_name='object_content_type_1'
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )

    objects = AccessControlListManager()

    class Meta:
        verbose_name = _('Access entry')
        verbose_name_plural = _('Access entries')

    def __str__(self):
        return '%s: %s' % (self.content_type, self.content_object)
'''
