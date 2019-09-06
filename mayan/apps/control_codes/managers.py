from __future__ import unicode_literals

from django.db import models


class ControlSheetCodeBusinessLogicManager(models.Manager):
    def enabled(self):
        return self.filter(enabled=True)
