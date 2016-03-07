# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core import checks
from django.db import models
from django.db.models.fields import FieldDoesNotExist


class CurrentOrganizationManager(models.Manager):
    "Use this to limit objects to those associated with the current organization."

    def __init__(self, field_name=None):
        super(CurrentOrganizationManager, self).__init__()
        self.__field_name = field_name

    def check(self, **kwargs):
        errors = super(CurrentOrganizationManager, self).check(**kwargs)
        errors.extend(self._check_field_name())
        return errors

    def _check_field_name(self):
        field_name = self._get_field_name()
        try:
            field = self.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return [
                checks.Error(
                    "CurrentOrganizationManager could not find a field named '%s'." % field_name,
                    hint=None,
                    obj=self,
                    id='organizations.E001',
                )
            ]

        if not isinstance(field, (models.ForeignKey, models.ManyToManyField)):
            return [
                checks.Error(
                    "CurrentOrganizationManager cannot use '%s.%s' as it is not a ForeignKey or ManyToManyField." % (
                        self.model._meta.object_name, field_name
                    ),
                    hint=None,
                    obj=self,
                    id='organizations.E002',
                )
            ]

        return []

    def _get_field_name(self):
        """ Return self.__field_name or 'organization' or 'organizations'. """

        if not self.__field_name:
            try:
                self.model._meta.get_field('organization')
            except FieldDoesNotExist:
                self.__field_name = 'organizations'
            else:
                self.__field_name = 'organization'
        return self.__field_name

    def get_queryset(self):
        return super(CurrentOrganizationManager, self).get_queryset().filter(
            **{self._get_field_name() + '__id': settings.ORGANIZATION_ID})
