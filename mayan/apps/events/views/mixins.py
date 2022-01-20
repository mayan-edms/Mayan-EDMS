from django.http import Http404

from ..classes import EventType
from ..literals import TEXT_UNKNOWN_EVENT_ID


class EventViewMixin:
    def get_event_type(self, id):
        try:
            return EventType.get(id=id)
        except KeyError:
            raise Http404(TEXT_UNKNOWN_EVENT_ID % id)
