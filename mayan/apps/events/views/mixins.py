from django.http import Http404

from ..classes import EventType
from ..literals import TEXT_UNKNOWN_EVENT_ID


class VerbEventViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.event_type = self.get_event_type()
        return super().dispatch(request=request, *args, **kwargs)

    def get_event_type(self):
        event_type_id = self.kwargs['verb']

        try:
            return EventType.get(id=event_type_id)
        except KeyError:
            raise Http404(TEXT_UNKNOWN_EVENT_ID % event_type_id)
