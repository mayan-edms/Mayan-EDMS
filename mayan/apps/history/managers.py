from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models


class ObjectHistoryManager(models.Manager):
    def get_url_for_object(self):
        ct = ContentType.objects.get_for_model(self.instance)
        return reverse('history_for_object', args=[ct, self.instance.pk])
