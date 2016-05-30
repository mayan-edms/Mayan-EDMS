from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from organizations.managers import CurrentOrganizationManager


class MessageManager(models.Manager):
    def get_for_now(self):
        now = timezone.now()
        return self.filter(enabled=True).filter(
            Q(start_datetime__isnull=True) | Q(start_datetime__lte=now)
        ).filter(Q(end_datetime__isnull=True) | Q(end_datetime__gte=now))


class OrganizationMessageManager(MessageManager, CurrentOrganizationManager):
    def get_queryset(self):
        return super(OrganizationMessageManager, self).get_queryset().filter(
            **{self._get_field_name() + '__id': settings.ORGANIZATION_ID}
        )
