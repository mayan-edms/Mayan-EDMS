from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AnonymousUser


class AnonymousUserSingletonManager(models.Manager):
    def passthru_check(self, user):
        if isinstance(user, AnonymousUser):
            return self.model.objects.get()
        else:
            return user
