from django.http import Http404

from mayan.apps.acls.models import AccessControlList

from ..classes import EventType
from ..literals import TEXT_UNKNOWN_EVENT_ID
from ..permissions import permission_events_view


class NotificationViewMixin:
    def get_source_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_events_view,
            queryset=self.request.user.notifications.all(),
            user=self.request.user
        )


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
