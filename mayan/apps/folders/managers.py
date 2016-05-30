from django.db import models


class FolderManager(models.Manager):
    def get_by_natural_key(self, label, *user_key):
        return self.get(label=label)
