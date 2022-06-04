from mayan.apps.rest_api.api_view_mixins import ExternalContentTypeObjectAPIViewMixin
from mayan.apps.rest_api import generics

from .permissions import (
    permission_error_log_entry_delete, permission_error_log_entry_view
)
from .serializers import ErrorLogPartitionEntrySerializer


class APIErrorLogPartitionEntryListView(
    ExternalContentTypeObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the object's error log entries
    """
    mayan_external_object_permissions = {
        'GET': (permission_error_log_entry_view,),
    }
    ordering_fields = ('id', 'datetime')
    serializer_class = ErrorLogPartitionEntrySerializer

    def get_queryset(self):
        return self.external_object.error_log.all()


class APIErrorLogPartitionEntryDetailView(
    ExternalContentTypeObjectAPIViewMixin, generics.RetrieveDestroyAPIView
):
    """
    delete: Delete the selected error log entry.
    get: Returns the details of the selected error log entry.
    """
    lookup_url_kwarg = 'error_log_partition_entry_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_error_log_entry_delete,),
        'GET': (permission_error_log_entry_view,)
    }
    serializer_class = ErrorLogPartitionEntrySerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.external_object.error_log.all()
