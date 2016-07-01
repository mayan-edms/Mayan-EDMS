from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from permissions.classes import Permission

from .settings import (
    setting_organization_admin_group, setting_organization_admin_email,
    setting_organization_admin_password, setting_organization_admin_role,
    setting_organization_admin_username
)

ORGANIZATION_CACHE = {}
logger = logging.getLogger(__name__)


class OrganizationManager(models.Manager):
    def get_current(self):
        """
        Returns the current ``Organization`` based on the ORGANIZATION_ID in
        the project's settings. The ``Organization`` object is cached the first
        time it's retrieved from the database.
        """
        try:
            oid = settings.ORGANIZATION_ID
        except AttributeError:
            raise ImproperlyConfigured(
                "You're using the \"organizations framework\" without "
                "having set the ORGANIZATION_ID setting. Create an "
                "organization in your database and set the ORGANIZATION_ID "
                "setting to fix this error."
            )
        try:
            current_organization = ORGANIZATION_CACHE[oid]
        except KeyError:
            current_organization = self.get(pk=oid)
            ORGANIZATION_CACHE[oid] = current_organization
        return current_organization

    def clear_cache(self):
        """Clears the ``Organization`` object cache."""
        global ORGANIZATION_CACHE
        ORGANIZATION_CACHE = {}


@python_2_unicode_compatible
class Organization(models.Model):
    label = models.CharField(max_length=50, verbose_name=_('Label'))
    objects = OrganizationManager()

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')
        ordering = ('label',)

    def __str__(self):
        return self.label

    def create_admin(self, email=setting_organization_admin_email.value, password=setting_organization_admin_password.value, username=setting_organization_admin_username.value):
        UserModel = get_user_model()

        if password:
            try:
                # Let's try to see if it is a callable
                password_value = password()
            except TypeError:
                password_value = password
        else:
            password_value = UserModel.objects.make_random_password()

        try:
            UserModel.objects.get(
                **{UserModel.USERNAME_FIELD: username, 'organization': self}
            )
        except UserModel.DoesNotExist:
            MayanGroup = apps.get_model('user_management', 'MayanGroup')
            Role = apps.get_model('permissions', 'Role')

            group, created = MayanGroup.objects.get_or_create(
                name=setting_organization_admin_group.value, organization=self
            )

            role, created = Role.objects.get_or_create(
                label=setting_organization_admin_role.value, organization=self
            )

            logger.info(
                'Creating organization admin -- login: %s, email: %s, '
                'password: %s', username, email, password_value
            )

            UserModel.objects.create(
                **{
                    'email': email,
                    'organization': self,
                    UserModel.USERNAME_FIELD: username
                }
            )

            account = UserModel.objects.get(
                **{UserModel.USERNAME_FIELD: username, 'organization': self}
            )
            account.set_password(raw_password=password_value)
            account.save()

            role.organization_groups.add(group)
            account.organization_groups.add(group)

            Permission.invalidate_cache()

            for permission in Permission.all():
                role.permissions.add(permission.stored_permission)

            Organization.objects.clear_cache()

            return account, password_value
        else:
            logger.error(
                'Organization admin user already exists. -- login: %s',
                username
            )


def clear_organization_cache(sender, **kwargs):
    """
    Clears the cache (if primed) each time a organization is saved or deleted
    """
    instance = kwargs['instance']
    try:
        del ORGANIZATION_CACHE[instance.pk]
    except KeyError:
        pass


pre_save.connect(clear_organization_cache, sender=Organization)
pre_delete.connect(clear_organization_cache, sender=Organization)
