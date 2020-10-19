import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.views.decorators.cache import cache_control, patch_cache_control

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from mayan.apps.rest_api import generics

from ..literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_view
)
from ..serializers.document_version_serializers import (
    DocumentVersionSerializer, DocumentVersionPageSerializer
)
from ..settings import setting_document_version_page_image_cache_time
from ..tasks import (
    task_document_version_export, task_document_version_page_image_generate
)

from .mixins import (
    ParentObjectDocumentAPIViewMixin, ParentObjectDocumentVersionAPIViewMixin
)

logger = logging.getLogger(name=__name__)


class APIDocumentVersionDetailView(
    ParentObjectDocumentAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected document version.
    get: Returns the selected document version details.
    patch: Edit the properties of the selected document version.
    put: Edit the properties of the selected document version.
    """
    lookup_url_kwarg = 'document_version_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_version_delete,),
        'GET': (permission_document_version_view,),
        'PATCH': (permission_document_version_edit,),
        'PUT': (permission_document_version_edit,)
    }
    serializer_class = DocumentVersionSerializer

    def get_queryset(self):
        return self.get_document().versions.all()


###
class SerializerActionAPIViewMixin:
    serializer_action_name = None

    def serializer_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_serializer_action(serializer=serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def perform_serializer_action(self, serializer):
        getattr(serializer, self.serializer_action_name)()

    def post(self, request, *args, **kwargs):
        return self.serializer_action(request=request, *args, **kwargs)


class ActionAPIViewMixin:
    action_response_status = None

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def perform_view_action(self):
        raise ImproperlyConfigured(
            'Need to specify the `.perform_action()` method.'
        )

    def post(self, request, *args, **kwargs):
        return self.view_action(request=request, *args, **kwargs)

    def view_action(self, request, *args, **kwargs):
        self.perform_view_action()
        return Response(
            status=self.action_response_status or status.HTTP_200_OK
        )


class APIDocumentVersionExportView(
    ActionAPIViewMixin, ParentObjectDocumentAPIViewMixin,
    generics.GenericAPIView
):
    """
    post: Exports the specified document version.
    """
    action_response_status = status.HTTP_202_ACCEPTED
    lookup_url_kwarg = 'document_version_id'
    mayan_object_permissions = {
        'POST': (permission_document_version_export,),
    }

    def get_queryset(self):
        return self.get_document().versions.all()

    def perform_view_action(self):
        task_document_version_export.apply_async(
            kwargs={'document_version_id': self.get_object().pk}
        )


class APIDocumentVersionListView(
    ParentObjectDocumentAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Return a list of the selected document's versions.
    post: Create a new document version.
    """
    #mayan_object_permissions = {
    #    'GET': (permission_document_version_view,),
    #    'POST': (permission_document_version_create,),
    #}
    serializer_class = DocumentVersionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.get_document()
        }

    def get_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_version_view
        else:
            permission = permission_document_version_create

        return self.get_document(permission=permission).versions.all()


class APIDocumentVersionPageListView(
    ParentObjectDocumentVersionAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns an list of the pages for the selected document version.
    """
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }
    serializer_class = DocumentVersionPageSerializer

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentVersionPageImageView(
    ParentObjectDocumentVersionAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected document version page.
    """
    lookup_url_kwarg = 'document_version_page_id'
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }

    def get_queryset(self):
        return self.get_document_version().pages.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    @cache_control(private=True)
    def retrieve(self, request, *args, **kwargs):
        width = request.GET.get('width')
        height = request.GET.get('height')
        zoom = request.GET.get('zoom')

        if zoom:
            zoom = int(zoom)

        rotation = request.GET.get('rotation')

        if rotation:
            rotation = int(rotation)

        maximum_layer_order = request.GET.get('maximum_layer_order')
        if maximum_layer_order:
            maximum_layer_order = int(maximum_layer_order)

        task = task_document_version_page_image_generate.apply_async(
            kwargs=dict(
                document_version_page_id=self.get_object().pk, width=width,
                height=height, zoom=zoom, rotation=rotation,
                maximum_layer_order=maximum_layer_order,
                user_id=request.user.pk
            )
        )

        kwargs = {'timeout': DOCUMENT_IMAGE_TASK_TIMEOUT}
        if settings.DEBUG:
            # In debug more, task are run synchronously, causing this method
            # to be called inside another task. Disable the check of nested
            # tasks when using debug mode.
            kwargs['disable_sync_subtasks'] = False

        cache_filename = task.get(**kwargs)
        cache_file = self.get_object().cache_partition.get_file(filename=cache_filename)
        with cache_file.open() as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response=response,
                    max_age=setting_document_version_page_image_cache_time.value
                )
            return response
