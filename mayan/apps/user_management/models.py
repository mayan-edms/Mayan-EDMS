from __future__ import unicode_literals

from django.contrib.auth.models import (
    AbstractUser, Group, GroupManager, UserManager
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from organizations.models import Organization
from organizations.managers import CurrentOrganizationManager
from organizations.shortcuts import get_current_organization


class MayanGroup(Group):
    organization = models.ForeignKey(
        Organization, default=get_current_organization
    )
    objects = GroupManager()
    on_organization = CurrentOrganizationManager()

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class OrganizationUserManagerHybridClass(CurrentOrganizationManager, UserManager):
    """
    Hybrid class to allow calling 'create_superuser' from 'on_organization'
    """


class MayanUser(AbstractUser):
    organization = models.ForeignKey(
        Organization, blank=True, default=get_current_organization, null=True
    )

    organization_groups = models.ManyToManyField(
        MayanGroup, blank=True, help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ), related_name='users', related_query_name='user',
        verbose_name=_('Groups')
    )

    objects = UserManager()
    on_organization = OrganizationUserManagerHybridClass()
