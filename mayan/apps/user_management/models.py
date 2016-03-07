from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from organizations.models import Organization
from organizations.managers import CurrentOrganizationManager
from organizations.shortcuts import get_current_organization


class MayanUser(AbstractUser):
    organization = models.ForeignKey(
        Organization, default=get_current_organization
    )

    objects = UserManager()
    on_organization = CurrentOrganizationManager()
