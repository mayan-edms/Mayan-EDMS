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
from ..serializers.document_file_serializers import (
    DocumentFileSerializer, DocumentFileCreateSerializer,
    DocumentFileWritableSerializer, DocumentFilePageSerializer
)
from ..settings import setting_document_file_page_image_cache_time
from ..tasks import task_document_file_page_image_generate

logger = logging.getLogger(name=__name__)


class APIDocumentFileDownloadView(DownloadMixin, generics.RetrieveAPIView):
    """
    get: Download a document file.
    """
    lookup_url_kwarg = 'document_file_id'

    def get_document(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_download,
            queryset=Document.objects.all(), user=self.request.user
        )

        return get_object_or_404(klass=queryset, pk=self.kwargs['document_id'])

    def get_download_file_object(self):
        instance = self.get_object()
        return instance.open()

    def get_download_filename(self):
        preserve_extension = self.request.GET.get(
            'preserve_extension', self.request.POST.get(
                'preserve_extension', False
            )
        )

        preserve_extension = preserve_extension == 'true' or preserve_extension == 'True'

        instance = self.get_object()
        return instance.get_rendered_string(
            preserve_extension=preserve_extension
        )

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def get_queryset(self):
        return self.get_document().files.all()

    def retrieve(self, request, *args, **kwargs):
        return self.render_to_response()


class APIDocumentFilePageImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document.
    """
    lookup_url_kwarg = 'document_file_page_id'

    def get_document(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_view, queryset=Document.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(klass=queryset, pk=self.kwargs['document_id'])

    def get_document_file(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_view,
            queryset=self.get_document().files.all(), user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['document_file_id']
        )

    def get_queryset(self):
        return self.get_document_file().pages.all()

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

        task = task_document_file_page_image_generate.apply_async(
            kwargs=dict(
                document_file_page_id=self.get_object().pk, width=width,
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
                    max_age=setting_document_file_page_image_cache_time.value
                )
            return response


class APIDocumentFilePageDetailView(generics.RetrieveAPIView):
    """
    get: Returns the selected document page details.
    """
    lookup_url_kwarg = 'document_file_page_id'
    serializer_class = DocumentFilePageSerializer

    def get_document(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_view,
            queryset=Document.objects.all(), user=self.request.user
        )

        return get_object_or_404(klass=queryset, pk=self.kwargs['document_id'])

    def get_document_file(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_file_view,
            queryset=Document.objects.all(), user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['document_file_id']
        )

    def get_queryset(self):
        return self.get_document_file().pages.all()


class APIDocumentFilePageListView(generics.ListAPIView):
    serializer_class = DocumentFilePageSerializer

    def get_document(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )
        return document

    def get_document_file(self):
        return get_object_or_404(
            self.get_document().files.all(), pk=self.kwargs['file_pk']
        )

    def get_queryset(self):
        return self.get_document_file().pages.all()


class APIDocumentFilesListView(generics.ListCreateAPIView):
    """
    get: Return a list of the selected document's files.
    post: Create a new document file.
    """
    mayan_object_permissions = {
        'GET': (permission_document_file_view,),
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_202_ACCEPTED, headers=headers)

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentFilesListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentFileSerializer
        elif self.request.method == 'POST':
            return DocumentFileCreateSerializer

    def get_queryset(self):
        return get_object_or_404(Document, pk=self.kwargs['document_id']).files.all()

    def perform_create(self, serializer):
        document = get_object_or_404(Document, pk=self.kwargs['document_id'])

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_file_new,),
            user=self.request.user,
        )
        serializer.save(document=document, _user=self.request.user)


class APIDocumentFileDetailView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete the selected document file.
    get: Returns the selected document file details.
    """
    lookup_url_kwarg = 'document_file_id'

    def get_queryset(self):
        if self.request.method == 'DELETE':
            permission_required = permission_document_file_delete
        else:
            permission_required = permission_document_file_view

        return AccessControlList.objects.restrict_queryset(
            permission=permission_required,
            queryset=DocumentFile.objects.all(), user=self.request.user
        )
        return self.get_document().files.all()


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentFileSerializer
        else:
            return DocumentFileWritableSerializer
