from __future__ import unicode_literals

from django.conf import settings

from model_utils.managers import InheritanceManager, InheritanceQuerySet

from organizations.managers import CurrentOrganizationManager


class OrganizationSourceManager(InheritanceManager, CurrentOrganizationManager):
    def get_queryset(self):
        return InheritanceQuerySet(self.model).filter(
            **{self._get_field_name() + '__id': settings.ORGANIZATION_ID}
        )
