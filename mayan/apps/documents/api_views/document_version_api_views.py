import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, patch_cache_control

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api import generics
from mayan.apps.views.generics import DownloadMixin

from ..literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from ..models.document_file_models import DocumentFile
from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..models.misc_models import DeletedDocument, RecentDocument
from ..permissions import (
    permission_document_create, permission_document_edit,
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_new,  permission_document_file_view,
    permission_document_properties_edit, permission_document_trash,
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
    permission_document_view, permission_trashed_document_delete,
    permission_trashed_document_restore
)
from ..serializers.document_version_serializers import (
    #DocumentVersionCreateSerializer,
    #DocumentVersionSerializer,
    #DocumentVersionWritableSerializer,
    DocumentVersionPageSerializer,
)
from ..settings import (
    setting_document_file_page_image_cache_time,
    setting_document_version_page_image_cache_time
)
from ..tasks import (
    task_document_file_page_image_generate,
    task_document_version_page_image_generate
)

logger = logging.getLogger(name=__name__)


class APIDocumentVersionPageListView(generics.ListAPIView):
    serializer_class = DocumentVersionPageSerializer

    def get_document(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_version_view,),
            user=self.request.user
        )
        return document

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs['version_pk']
        )

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentVersionPageImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document version page.
    """
    lookup_url_kwarg = 'document_version_page_id'

    def get_document(self):
        document = get_object_or_404(
            Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )
        return document

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs[
                'document_version_id'
            ]
        )

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
