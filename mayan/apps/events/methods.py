from django.apps import apps

from .classes import EventType


def method_action_get_extra_data(self):
    Action = apps.get_model(app_label='actstream', model_name='Action')

    try:
        return self.extra_data.loads()
    except Action.extra_data.RelatedObjectDoesNotExist:
        return {}


def method_action_get_event_type(self):
    return EventType.get(name=self.verb)
