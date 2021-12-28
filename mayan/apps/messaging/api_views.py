from mayan.apps.rest_api import generics

from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)
from .serializers import MessageSerializer


class APIMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected message.
    get: Return the details of the selected message.
    patch: Partially edit the selected message.
    put: Edit the selected message.
    """
    lookup_url_kwarg = 'message_id'
    mayan_object_permissions = {
        'GET': (permission_message_view,),
        'PUT': (permission_message_edit,),
        'PATCH': (permission_message_edit,),
        'DELETE': (permission_message_delete,)
    }
    serializer_class = MessageSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.request.user.messages.all()


class APIMessageListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the messages.
    post: Create a new message.
    """
    mayan_object_permissions = {'GET': (permission_message_view,)}
    mayan_view_permissions = {'POST': (permission_message_create,)}
    ordering_fields = ('date_time', 'id')
    serializer_class = MessageSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.request.user.messages.all()
