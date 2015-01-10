from django.contrib.contenttypes.models import ContentType
from django.db import models


class EventTypeManager(models.Manager):
    def create(self, *args, **kwargs):
        label = kwargs.pop('label')

        instance = super(EventTypeManager, self).create(*args, **kwargs)
        self.model._labels[instance.name] = label
        return instance

    def get(self, *args, **kwargs):
        instance = super(EventTypeManager, self).get(*args, **kwargs)
        instance.label = self.model._labels[instance.name]
        return instance

    def get_or_create(self, *args, **kwargs):
        label = kwargs.pop('label')

        instance, boolean = super(EventTypeManager, self).get_or_create(*args, **kwargs)
        self.model._labels[instance.name] = label
        return instance, boolean
