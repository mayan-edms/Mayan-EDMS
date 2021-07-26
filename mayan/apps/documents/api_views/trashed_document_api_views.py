import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.cache import cache_control, patch_cache_control

from mayan.apps.converter.tasks import task_content_object_image_generate
from mayan.apps.rest_api import generics

from ..literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from ..models.trashed_document_models import TrashedDocument
from ..permissions import (
    permission_document_version_view, permission_document_view,
    permission_trashed_document_delete, permission_trashed_document_restore
)
from ..serializers.trashed_document_serializers import TrashedDocumentSerializer
from ..settings import setting_document_version_page_image_cache_time

logger = logging.getLogger(name=__name__)


class APITrashedDocumentDetailView(generics.RetrieveDestroyAPIView):
    """
    Returns the selected trashed document details.
    delete: Delete the trashed document.
    get: Retreive the details of the trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'DELETE': (permission_trashed_document_delete,),
        'GET': (permission_document_view,)
    }
    queryset = TrashedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APITrashedDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the trashed documents.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    ordering_fields = ('id', 'label')
    queryset = TrashedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentRestoreView(generics.ObjectActionAPIView):
    """
    post: Restore a trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_trashed_document_restore,)
    }
    queryset = TrashedDocument.objects.all()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def object_action(self, request, serializer):
        self.object.restore()


class APITrashedDocumentImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }

    def get_queryset(self):
        return TrashedDocument.objects.all()

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

        obj = self.get_object().version_active.pages.first()

        content_type = ContentType.objects.get_for_model(model=obj)

        task = task_content_object_image_generate.apply_async(
            kwargs={
                'content_type_id': content_type.pk,
                'object_id': obj.pk,
                'height': height,
                'maximum_layer_order': maximum_layer_order,
                'rotation': rotation,
                'user_id': request.user.pk,
                'width': width,
                'zoom': zoom
            }
        )

        kwargs = {'timeout': DOCUMENT_IMAGE_TASK_TIMEOUT}
        if settings.DEBUG:
            # In debug more, task are run synchronously, causing this method
            # to be called inside another task. Disable the check of nested
            # tasks when using debug mode.
            kwargs['disable_sync_subtasks'] = False

        cache_filename = task.get(**kwargs)
        cache_file = obj.cache_partition.get_file(filename=cache_filename)
        with cache_file.open() as file_object:
            response = HttpResponse(content=file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response=response,
                    max_age=setting_document_version_page_image_cache_time.value
                )
            return response
