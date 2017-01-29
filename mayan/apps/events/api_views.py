from __future__ import unicode_literals

from actstream.models import Action
from rest_framework import generics

from rest_api.permissions import MayanPermission

from .classes import Event
from .permissions import permission_events_view
from .serializers import EventSerializer, EventTypeSerializer


class APIEventTypeListView(generics.ListAPIView):
    """
    Returns a list of all the available event types.
    """

    serializer_class = EventTypeSerializer
    queryset = sorted(Event.all(), key=lambda event: event.name)


class APIEventListView(generics.ListAPIView):
    """
    Returns a list of all the available events.
    """

    mayan_view_permissions = {'GET': (permission_events_view,)}
    permission_classes = (MayanPermission,)
    queryset = Action.objects.all()
    serializer_class = EventSerializer
