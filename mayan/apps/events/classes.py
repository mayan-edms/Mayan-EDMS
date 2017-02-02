from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from actstream import action


class Event(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(
                _('Unknown or obsolete event type: {0}'.format(name))
            )

    @classmethod
    def get_label(cls, name):
        try:
            return cls.get(name=name).label
        except KeyError as exception:
            return unicode(exception)

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.event_type = None
        self.__class__._registry[name] = self

    def get_type(self):
        if not self.event_type:
            EventType = apps.get_model('events', 'EventType')

            self.event_type, created = EventType.objects.get_or_create(
                name=self.name
            )

        return self.event_type

    def commit(self, actor=None, action_object=None, target=None):
        if not self.event_type:
            EventType = apps.get_model('events', 'EventType')
            self.event_type, created = EventType.objects.get_or_create(
                name=self.name
            )

        action.send(
            actor or target, actor=actor, verb=self.name,
            action_object=action_object, target=target
        )
