from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models


class EventSubscriptionManager(models.Manager):
    def create_for(self, stored_event_type, user):
        return self.create(
            stored_event_type=stored_event_type, user=user
        )

    def get_for(self, stored_event_type, user):
        return self.filter(
            stored_event_type=stored_event_type, user=user
        )


class ObjectEventSubscriptionManager(models.Manager):
    def create_for(self, obj, stored_event_type, user):
        content_type = ContentType.objects.get_for_model(model=obj)

        return self.create(
            content_type=content_type, object_id=obj.pk,
            stored_event_type=stored_event_type, user=user
        )

    def get_for(self, obj, stored_event_type, user):
        content_type = ContentType.objects.get_for_model(model=obj)

        return self.filter(
            content_type=content_type, object_id=obj.pk,
            stored_event_type=stored_event_type, user=user
        )
