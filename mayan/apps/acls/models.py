import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions.models import Role, StoredPermission

from .events import event_acl_created, event_acl_edited
from .managers import AccessControlListManager

logger = logging.getLogger(name=__name__)


@python_2_unicode_compatible
class AccessControlList(models.Model):
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
        on_delete=models.CASCADE, related_name='acls', to=Role,
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

    def get_absolute_url(self):
        return reverse(
            viewname='acls:acl_permissions', kwargs={'acl_id': self.pk}
        )

    def get_inherited_permissions(self):
        return AccessControlList.objects.get_inherited_permissions(
            obj=self.content_object, role=self.role
        )

    def permissions_add(self, queryset, _user=None):
        with transaction.atomic():
            event_acl_edited.commit(
                actor=_user, target=self
            )
            self.permissions.add(*queryset)

    def permissions_remove(self, queryset, _user=None):
        with transaction.atomic():
            event_acl_edited.commit(
                actor=_user, target=self
            )
            self.permissions.remove(*queryset)

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            super(AccessControlList, self).save(*args, **kwargs)
            if is_new:
                event_acl_created.commit(
                    actor=_user, target=self
                )
            else:
                event_acl_edited.commit(
                    actor=_user, target=self
                )
