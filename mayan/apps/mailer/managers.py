from django.db import models


class UserMailerManager(models.Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)
