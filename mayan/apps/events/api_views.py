from django.http import Http404

from actstream.models import Action, any_stream

from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalContentTypeObjectAPIViewMixin

from .classes import EventType, EventTypeNamespace
from .models import Notification
from .permissions import permission_events_view
from .serializers import (
    EventSerializer, EventTypeSerializer, EventTypeNamespaceSerializer,
    NotificationSerializer
)


class APIObjectEventListView(
    ExternalContentTypeObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Return a list of events for the specified object.
    """
    mayan_external_object_permissions = {
        'GET': (permission_events_view,),
    }
    ordering_fields = ('id', 'timestamp')
    serializer_class = EventSerializer

    def get_queryset(self):
        return any_stream(obj=self.external_object)


class APIEventTypeNamespaceDetailView(generics.RetrieveAPIView):
    """
    get: Returns the details of an event type namespace.
    """
    serializer_class = EventTypeNamespaceSerializer

    def get_object(self):
        try:
            return EventTypeNamespace.get(name=self.kwargs['name'])
        except KeyError:
            raise Http404


class APIEventTypeNamespaceListView(generics.ListAPIView):
    """
    get: Returns a list of all the available event type namespaces.
    """
    serializer_class = EventTypeNamespaceSerializer
    queryset = EventTypeNamespace.all()

    def get_serializer_context(self):
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }


class APIEventTypeNamespaceEventTypeListView(generics.ListAPIView):
    """
    get: Returns a list of all the available event types from a namespaces.
    """
    serializer_class = EventTypeSerializer

    def get_queryset(self):
        try:
            return EventTypeNamespace.get(
                name=self.kwargs['name']
            ).get_event_types()
        except KeyError:
            raise Http404

    def get_serializer_context(self):
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }


class APIEventTypeListView(generics.ListAPIView):
    """
    get: Returns a list of all the available event types.
    """
    serializer_class = EventTypeSerializer
    queryset = EventType.all()

    def get_serializer_context(self):
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }


class APIEventListView(generics.ListAPIView):
    """
    get: Returns a list of all the available events.
    """
    mayan_view_permissions = {'GET': (permission_events_view,)}
    ordering_fields = ('id', 'timestamp')
    queryset = Action.objects.all()
    serializer_class = EventSerializer

    def get_serializer_context(self):
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }


class APINotificationListView(generics.ListAPIView):
    """
    get: Return a list of notifications for the current user.
    """
    ordering_fields = ('action__timestamp', 'id', 'read')
    serializer_class = NotificationSerializer

    def get_queryset(self):
        parameter_read = self.request.GET.get('read')

        if self.request.user.is_authenticated:
            queryset = Notification.objects.filter(user=self.request.user)
        else:
            queryset = Notification.objects.none()

        if parameter_read == 'True':
            queryset = queryset.filter(read=True)
        elif parameter_read == 'False':
            queryset = queryset.filter(read=False)

        return queryset
