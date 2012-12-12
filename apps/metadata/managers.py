from __future__ import absolute_import

from django.db import models


class MetadataTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class MetadataSetManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)
