from rest_framework import status
from rest_framework.response import Response

from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.rest_api import generics

from .models import Source
from .permissions import (
    permission_sources_create, permission_sources_delete,
    permission_sources_edit, permission_sources_view
)
from .serializers import SourceBackendActionSerializer, SourceSerializer


class APISourceListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the source.
    post: Create a new source.
    """
    mayan_object_permissions = {
        'GET': (permission_sources_view,)
    }
    mayan_view_permissions = {
        'POST': (permission_sources_create,)
    }
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APISourceView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected source.
    get: Details of the selected source.
    patch: Edit the selected source.
    put: Edit the selected source.
    """
    lookup_url_kwarg = 'source_id'
    mayan_object_permissions = {
        'DELETE': (permission_sources_delete,),
        'GET': (permission_sources_view,),
        'PATCH': (permission_sources_edit,),
        'PUT': (permission_sources_edit,)
    }
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APISourceActionView(generics.ObjectActionAPIView):
    """
    get: Get data from a source action.
    post: Execute a source action.
    """
    lookup_url_kwarg = 'source_id'
    mayan_object_permissions = {
        'GET': (permission_document_create,),
        'POST': (permission_document_create,)
    }
    serializer_class = SourceBackendActionSerializer

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request=request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.get_action().confirmation:
            handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)
            self.response = self.finalize_response(
                request, response, *args, **kwargs
            )
            return self.response
        else:
            return self.view_action(request, *args, **kwargs)

    def get_action(self):
        return self.object.get_action(name=self.kwargs['action_name'])

    def get_queryset(self):
        return Source.objects.filter(enabled=True)

    def object_action(self, request, serializer):
        query_dict = request.GET

        arguments = serializer.data.get('arguments', {}) or {}
        arguments.update(query_dict)

        return self.object.execute_action(
            name=self.kwargs['action_name'], request=request, **arguments
        ) or (None, None)

    def post(self, request, *args, **kwargs):
        if not self.get_action().confirmation:
            handler = self.http_method_not_allowed
            response = handler(request, *args, **kwargs)
            self.response = self.finalize_response(
                request, response, *args, **kwargs
            )
            return self.response
        else:
            return self.view_action(request, *args, **kwargs)

    def view_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(self.object, key, value)

        data, response = self.object_action(
            request=request, serializer=serializer
        )

        if response:
            return response
        else:
            if data:
                # If object action returned serializer.data.
                headers = self.get_success_headers(data=data)
                return Response(
                    data=data, status=status.HTTP_200_OK, headers=headers
                )
            else:
                return Response(status=status.HTTP_200_OK)
