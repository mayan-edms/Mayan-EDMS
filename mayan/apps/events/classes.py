from __future__ import absolute_import

from django.core import serializers
from django.db import models

from actstream import action


class Event(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.event_type = None

    def commit(self, actor=None, action_object=None, target=None):
        model = models.get_model('events', 'EventType')

        if not self.event_type:
            self.event_type, created = model.objects.get_or_create(
                label=self.label, name=self.name)

        action.send(actor or target, actor=actor, verb=self.name, action_object=action_object, target=target)
