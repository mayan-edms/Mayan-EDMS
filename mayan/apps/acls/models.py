from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
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
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id',
    )
    # TODO: limit choices to the permissions valid for the content_object
    permissions = models.ManyToManyField(
        StoredPermission, blank=True, related_name='acls',
        verbose_name=_('Permissions')
    )
    role = models.ForeignKey(Role, related_name='acls', verbose_name=_('Role'))

    objects = AccessControlListManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'role')
        verbose_name = _('Access entry')
        verbose_name_plural = _('Access entries')

    def __str__(self):
        return _('Permissions "%(permissions)s" to role "%(role)s" for "%(object)s"') % {
            'permissions': self.get_permission_titles(),
            'object': self.content_object,
            'role': self.role
        }

    def get_inherited_permissions(self):
        return AccessControlList.objects.get_inherited_permissions(
            role=self.role, obj=self.content_object
        )

    def get_permission_titles(self):
        result = ', '.join(
            [unicode(permission) for permission in self.permissions.all()]
        )

        return result or _('None')
