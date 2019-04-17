from __future__ import unicode_literals

import logging

from django.db import models

logger = logging.getLogger(__name__)


class RoleManager(models.Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)


class StoredPermissionManager(models.Manager):
    def get_by_natural_key(self, namespace, name):
        return self.get(namespace=namespace, name=name)

    def purge_obsolete(self):
        for permission in self.all():
            try:
                permission.volatile_permission
            except KeyError:
                permission.delete()
