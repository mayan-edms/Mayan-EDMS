from __future__ import absolute_import, unicode_literals

from mayan.apps.rest_api import generics

from .models import Message
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)
from .serializers import MessageSerializer


class APIMessageListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the messages.
    post: Create a new message.
    """
    mayan_object_permissions = {'GET': (permission_message_view,)}
    mayan_view_permissions = {'POST': (permission_message_create,)}
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class APIMessageView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected message.
    get: Return the details of the selected message.
    patch: Edit the selected message.
    put: Edit the selected message.
    """
    mayan_object_permissions = {
        'DELETE': (permission_message_delete,),
        'GET': (permission_message_view,),
        'PATCH': (permission_message_edit,),
        'PUT': (permission_message_edit,)
    }
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
