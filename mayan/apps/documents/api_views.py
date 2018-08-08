from __future__ import absolute_import, unicode_literals

import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, patch_cache_control

from django_downloadview import DownloadMixin, VirtualFile
from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessControlList
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from .models import (
    Document, DocumentType, RecentDocument
)
from .permissions import (
    permission_document_create, permission_document_delete,
    permission_document_download, permission_document_edit,
    permission_document_new_version, permission_document_properties_edit,
    permission_document_restore, permission_document_trash,
    permission_document_view, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_document_version_revert,
    permission_document_version_view
)
from .serializers import (
    DeletedDocumentSerializer, DocumentPageSerializer, DocumentSerializer,
    DocumentTypeSerializer, DocumentVersionSerializer,
    NewDocumentSerializer, NewDocumentVersionSerializer,
    RecentDocumentSerializer, WritableDocumentSerializer,
    WritableDocumentTypeSerializer, WritableDocumentVersionSerializer
)
from .settings import settings_document_page_image_cache_time
from .storages import storage_documentimagecache
from .tasks import task_generate_document_page_image

logger = logging.getLogger(__name__)


class APIDeletedDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the trashed documents.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    permission_classes = (MayanPermission,)
    queryset = Document.trash.all()
    serializer_class = DeletedDocumentSerializer


class APIDeletedDocumentView(generics.RetrieveDestroyAPIView):
    """
    Returns the selected trashed document details.
    delete: Delete the trashed document.
    get: Retreive the details of the trashed document.
    """
    mayan_object_permissions = {
        'DELETE': (permission_document_delete,),
        'GET': (permission_document_view,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.trash.all()
    serializer_class = DeletedDocumentSerializer


class APIDeletedDocumentRestoreView(generics.GenericAPIView):
    """
    post: Restore a trashed document.
    """
    mayan_object_permissions = {
        'POST': (permission_document_restore,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.trash.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, *args, **kwargs):
        self.get_object().restore()
        return Response(status=status.HTTP_200_OK)


class APIDocumentDownloadView(DownloadMixin, generics.RetrieveAPIView):
    """
    get: Download the latest version of a document.
    """
    mayan_object_permissions = {
        'GET': (permission_document_download,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()

    def get_encoding(self):
        return self.get_object().latest_version.encoding

    def get_file(self):
        instance = self.get_object()
        return VirtualFile(instance.latest_version.file, name=instance.label)

    def get_mimetype(self):
        return self.get_object().latest_version.mimetype

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def retrieve(self, request, *args, **kwargs):
        return self.render_to_response()


class APIDocumentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the documents.
    post: Create a new document.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        elif self.request.method == 'POST':
            return NewDocumentSerializer

    def perform_create(self, serializer):
        AccessControlList.objects.check_access(
            permissions=(permission_document_create,), user=self.request.user,
            obj=serializer.validated_data['document_type']
        )
        serializer.save(_user=self.request.user)


class APIDocumentPageImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document.
    """
    lookup_url_kwarg = 'page_pk'

    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_view
        else:
            permission_required = permission_document_edit

        document = get_object_or_404(Document.passthrough, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permission_required, self.request.user, document
        )
        return document

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs['version_pk']
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

        task = task_generate_document_page_image.apply_async(
            kwargs=dict(
                document_page_id=self.get_object().pk, width=width,
                height=height, zoom=zoom, rotation=rotation
            )
        )

        cache_filename = task.get(timeout=DOCUMENT_IMAGE_TASK_TIMEOUT)
        with storage_documentimagecache.open(cache_filename) as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response, max_age=settings_document_page_image_cache_time.value
                )
            return response


class APIDocumentPageView(generics.RetrieveUpdateAPIView):
    """
    get: Returns the selected document page details.
    patch: Edit the selected document page.
    put: Edit the selected document page.
    """
    lookup_url_kwarg = 'page_pk'
    serializer_class = DocumentPageSerializer

    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_view
        else:
            permission_required = permission_document_edit

        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permission_required, self.request.user, document
        )
        return document

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs['version_pk']
        )

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the document types.
    post: Create a new document type.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_type_view,)}
    mayan_view_permissions = {'POST': (permission_document_type_create,)}
    permission_classes = (MayanPermission,)
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTypeListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeSerializer
        else:
            return WritableDocumentTypeSerializer


class APIDocumentTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected document type.
    get: Return the details of the selected document type.
    patch: Edit the properties of the selected document type.
    put: Edit the properties of the selected document type.
    """
    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
        'PUT': (permission_document_type_edit,),
        'PATCH': (permission_document_type_edit,),
        'DELETE': (permission_document_type_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = DocumentType.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTypeView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeSerializer
        else:
            return WritableDocumentTypeSerializer


class APIDocumentTypeDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents of a particular document type.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['pk'])
        AccessControlList.objects.check_access(
            permissions=permission_document_type_view, user=self.request.user,
            obj=document_type
        )

        return document_type.documents.all()


class APIDocumentVersionDownloadView(DownloadMixin, generics.RetrieveAPIView):
    """
    get: Download a document version.
    """
    lookup_url_kwarg = 'version_pk'

    def get_document(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=(permission_document_download,), user=self.request.user,
            obj=document
        )
        return document

    def get_encoding(self):
        return self.get_object().encoding

    def get_file(self):
        preserve_extension = self.request.GET.get(
            'preserve_extension', self.request.POST.get(
                'preserve_extension', False
            )
        )

        preserve_extension = preserve_extension == 'true' or preserve_extension == 'True'

        instance = self.get_object()
        return VirtualFile(
            instance.file, name=instance.get_rendered_string(
                preserve_extension=preserve_extension
            )
        )

    def get_mimetype(self):
        return self.get_object().mimetype

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def get_queryset(self):
        return self.get_document().versions.all()

    def retrieve(self, request, *args, **kwargs):
        return self.render_to_response()


class APIDocumentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document details.
    delete: Move the selected document to the thrash.
    get: Return the details of the selected document.
    patch: Edit the properties of the selected document.
    put: Edit the properties of the selected document.
    """
    mayan_object_permissions = {
        'GET': (permission_document_view,),
        'PUT': (permission_document_properties_edit,),
        'PATCH': (permission_document_properties_edit,),
        'DELETE': (permission_document_trash,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentView, self).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        else:
            return WritableDocumentSerializer


class APIRecentDocumentListView(generics.ListAPIView):
    """
    get: Return a list of the recent documents for the current user.
    """
    serializer_class = RecentDocumentSerializer

    def get_queryset(self):
        return RecentDocument.objects.filter(user=self.request.user)


class APIDocumentVersionPageListView(generics.ListAPIView):
    serializer_class = DocumentPageSerializer

    def get_document(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permission_document_view, self.request.user, document
        )
        return document

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs['version_pk']
        )

    def get_queryset(self):
        return self.get_document_version().pages.all()


class APIDocumentVersionsListView(generics.ListCreateAPIView):
    """
    get: Return a list of the selected document's versions.
    post: Create a new document version.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }
    mayan_permission_attribute_check = 'document'
    permission_classes = (MayanPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_202_ACCEPTED, headers=headers)

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentVersionsListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentVersionSerializer
        elif self.request.method == 'POST':
            return NewDocumentVersionSerializer

    def get_queryset(self):
        return get_object_or_404(Document, pk=self.kwargs['pk']).versions.all()

    def perform_create(self, serializer):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=(permission_document_new_version,),
            user=self.request.user, obj=document
        )
        serializer.save(document=document, _user=self.request.user)


class APIDocumentVersionView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected document version.
    get: Returns the selected document version details.
    patch: Edit the selected document version.
    put: Edit the selected document version.
    """
    lookup_url_kwarg = 'version_pk'

    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_view
        elif self.request.method == 'DELETE':
            permission_required = permission_document_version_revert
        else:
            permission_required = permission_document_edit

        document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permission_required, self.request.user, document
        )
        return document

    def get_queryset(self):
        return self.get_document().versions.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentVersionView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentVersionSerializer
        else:
            return WritableDocumentVersionSerializer
