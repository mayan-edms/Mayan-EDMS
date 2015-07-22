from __future__ import unicode_literals

import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


class StoredPermissionManager(models.Manager):
    def get_for_holder(self, holder):
        ct = ContentType.objects.get_for_model(holder)
        return self.model.objects.filter(
            permissionholder__holder_type=ct
        ).filter(permissionholder__holder_id=holder.pk)
