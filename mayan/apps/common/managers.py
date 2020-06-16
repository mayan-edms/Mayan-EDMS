from django.contrib.auth import get_user_model
from django.db import models


class UserLocaleProfileManager(models.Manager):
    def get_by_natural_key(self, user_natural_key):
        User = get_user_model()
        try:
            user = User.objects.get_by_natural_key(user_natural_key)
        except User.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(user__pk=user.pk)
