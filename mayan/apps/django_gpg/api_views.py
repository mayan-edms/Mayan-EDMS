from mayan.apps.rest_api import generics

from .models import Key
from .permissions import (
    permission_key_delete, permission_key_upload, permission_key_view
)
from .serializers import KeySerializer


class APIKeyListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the keys.
    post: Upload a new key.
    """
    mayan_object_permissions = {'GET': (permission_key_view,)}
    mayan_view_permissions = {'POST': (permission_key_upload,)}
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIKeyView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete the selected key.
    get: Return the details of the selected key.
    """
    lookup_url_kwarg = 'key_id'
    mayan_object_permissions = {
        'DELETE': (permission_key_delete,),
        'GET': (permission_key_view,),
    }
    queryset = Key.objects.all()
    serializer_class = KeySerializer
