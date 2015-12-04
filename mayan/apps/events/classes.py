from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from actstream import action


class Event(object):
    _labels = {}

    @classmethod
    def get_label(cls, name):
        try:
            return cls._labels[name]
        except KeyError:
            return _('Unknown or obsolete event type: {0}'.format(name))

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.event_type = None
        self.__class__._labels[name] = label

    def commit(self, actor=None, action_object=None, target=None):
        model = apps.get_model('events', 'EventType')

        if not self.event_type:
            self.event_type, created = model.objects.get_or_create(
                name=self.name
            )

        action.send(
            actor or target, actor=actor, verb=self.name,
            action_object=action_object, target=target
        )
