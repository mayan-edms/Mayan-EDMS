from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class OrganizationSmartLinkConditionManager(models.Manager):
    def get_queryset(self):
        SmartLink = apps.get_model('linking', 'SmartLink')

        return super(
            OrganizationSmartLinkConditionManager, self
        ).get_queryset().filter(
            smart_link__in=SmartLink.on_organization.all(),
        )
