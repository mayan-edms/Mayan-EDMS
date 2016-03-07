from __future__ import unicode_literals

import string
import warnings

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.deprecation import RemovedInDjango19Warning
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

ORGANIZATION_CACHE = {}


class OrganizationManager(models.Manager):
    def get_current(self):
        """
        Returns the current ``Organization`` based on the ORGANIZATION_ID in
        the project's settings. The ``Organization`` object is cached the first
        time it's retrieved from the database.
        """
        from django.conf import settings
        try:
            oid = settings.ORGANIZATION_ID
        except AttributeError:
            raise ImproperlyConfigured(
                "You're using the Django \"organizations framework\" without "
                "having set the ORGANIZATION_ID setting. Create a site in "
                "your database and set the SITE_ID setting to fix this error."
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
