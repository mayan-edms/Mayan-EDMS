from __future__ import unicode_literals

from rest_framework import generics

from .classes import Event
from .serializers import EventSerializer


class APIEventTypeList(generics.ListAPIView):
    """
    Returns a list of all the available event types.
    """

    serializer_class = EventSerializer
    queryset = sorted(Event.all(), key=lambda event: event.name)
