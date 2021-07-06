from mayan.apps.rest_api import generics

from .models import Announcement
from .permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view
)
from .serializers import AnnouncementSerializer


class APIAnnouncementListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the announcements.
    post: Create a new announcement.
    """
    mayan_object_permissions = {'GET': (permission_announcement_view,)}
    mayan_view_permissions = {'POST': (permission_announcement_create,)}
    ordering_fields = (
        'enabled', 'end_datetime', 'id', 'label', 'start_datetime'
    )
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIAnnouncementView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected announcement.
    get: Return the details of the selected announcement.
    patch: Edit the selected announcement.
    put: Edit the selected announcement.
    """
    lookup_url_kwarg = 'announcement_id'
    mayan_object_permissions = {
        'DELETE': (permission_announcement_delete,),
        'GET': (permission_announcement_view,),
        'PATCH': (permission_announcement_edit,),
        'PUT': (permission_announcement_edit,)
    }
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }
