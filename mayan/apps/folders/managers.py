from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.db import models


class FolderManager(models.Manager):
    def get_by_natural_key(self, label, *user_key):
        user = get_user_model().objects.get_by_natural_key(*user_key)
        return self.get(label=label, user=user)
