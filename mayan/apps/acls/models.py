import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.permissions.models import Role, StoredPermission

from .events import event_acl_created, event_acl_deleted, event_acl_edited
from .managers import AccessControlListManager

logger = logging.getLogger(name=__name__)


class AccessControlList(ExtraDataModelMixin, models.Model):
    """
    ACL means Access Control List it is a more fine-grained method of
    granting access to objects. In the case of ACLs, they grant access using
    3 elements: actor, permission, object. In this case the actor is the role,
    the permission is the Mayan permission and the object can be anything:
    a document, a folder, an index, etc. This means = "Grant X permissions
    to role Y for object Z". This model holds the permission, object, actor
    relationship for one access control list.
    Fields:
    * Role - Custom role that is being granted a permission. Roles are created
    in the Setup menu.
    """
    content_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='object_content_type',
        to=ContentType
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id',
    )
    permissions = models.ManyToManyField(
        blank=True, related_name='acls', to=StoredPermission,
        verbose_name=_('Permissions')
    )
    role = models.ForeignKey(
        help_text=_(
            'Role to which the access is granted for the specified object.'
        ), on_delete=models.CASCADE, related_name='acls', to=Role,
        verbose_name=_('Role')
    )

    objects = AccessControlListManager()

    class Meta:
        ordering = ('pk',)
        unique_together = ('content_type', 'object_id', 'role')
        verbose_name = _('Access entry')
        verbose_name_plural = _('Access entries')

    def __str__(self):
        return _(
            'Role "%(role)s" permission\'s for "%(object)s"'
        ) % {
            'object': self.content_object,
            'role': self.role,
        }

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_acl_deleted,
        target='content_object'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            viewname='acls:acl_permissions', kwargs={'acl_id': self.pk}
        )

    def get_inherited_permissions(self):
        return AccessControlList.objects.get_inherited_permissions(
            obj=self.content_object, role=self.role
        )

    def permissions_add(self, queryset, _event_actor=None):
        for obj in queryset:
            self.permissions.add(obj)
            event_acl_edited.commit(
                action_object=obj, actor=_event_actor or self._event_actor,
                target=self
            )

    def permissions_remove(self, queryset, _event_actor=None):
        for obj in queryset:
            self.permissions.remove(obj)
            event_acl_edited.commit(
                action_object=obj, actor=_event_actor or self._event_actor,
                target=self
            )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'content_object',
            'event': event_acl_created,
            'target': 'self',
        },
        edited={
            'action_object': 'content_object',
            'event': event_acl_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class GlobalAccessControlListProxy(AccessControlList):
    class Meta:
        proxy = True
