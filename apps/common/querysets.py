from __future__ import absolute_import

from django.db.models.query import QuerySet

from .managers import CustomizableQuerySetManager


class CustomizableQuerySet(QuerySet):
    """Base QuerySet class for adding custom methods that are made
    available on both the manager and subsequent cloned QuerySets"""

    @classmethod
    def as_manager(cls, ManagerClass=CustomizableQuerySetManager):
        return ManagerClass(cls)
