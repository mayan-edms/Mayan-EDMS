from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessEntry
from converter.exceptions import UnkownConvertError, UnknownFileFormat
from converter.literals import (DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION,
                                DEFAULT_ZOOM_LEVEL)
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Document, DocumentPage, DocumentType, DocumentVersion
from .permissions import (PERMISSION_DOCUMENT_CREATE,
                          PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_EDIT,
                          PERMISSION_DOCUMENT_NEW_VERSION,
                          PERMISSION_DOCUMENT_PROPERTIES_EDIT,
                          PERMISSION_DOCUMENT_VIEW,
                          PERMISSION_DOCUMENT_TYPE_CREATE,
                          PERMISSION_DOCUMENT_TYPE_DELETE,
                          PERMISSION_DOCUMENT_TYPE_EDIT,
                          PERMISSION_DOCUMENT_TYPE_VIEW)
from .serializers import (DocumentImageSerializer, DocumentPageSerializer,
                          DocumentSerializer, DocumentTypeSerializer,
                          DocumentVersionSerializer)
from .settings import DISPLAY_SIZE, ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL
from .tasks import task_get_document_image

DOCUMENT_IMAGE_TASK_TIMEOUT = 10


class APIDocumentListView(generics.ListCreateAPIView):
    """
    Returns a list of all the documents.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_CREATE]}


class APIDocumentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document details.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_DOCUMENT_VIEW],
        'PUT': [PERMISSION_DOCUMENT_PROPERTIES_EDIT],
        'PATCH': [PERMISSION_DOCUMENT_PROPERTIES_EDIT],
        'DELETE': [PERMISSION_DOCUMENT_DELETE]
    }


class APIDocumentVersionCreateView(generics.CreateAPIView):
    """
    Create a new document version.
    """

    serializer_class = DocumentVersionSerializer
    queryset = DocumentVersion.objects.all()

    permission_classes = (MayanPermission,)
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_NEW_VERSION]}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            # Nested resource we take the document pk from the URL and insert it
            # so that it needs not to be specified by the user, we mark it as
            # a read only field in the serializer
            serializer.object.document = get_object_or_404(Document, pk=kwargs['pk'])

            try:
                # Check the uniqueness of this version for this document instead
                # of letting Django explode with an IntegrityError
                DocumentVersion.objects.get(
                    document=serializer.object.document,
                    major=serializer.object.major,
                    minor=serializer.object.minor,
                    micro=serializer.object.micro,
                    release_level=serializer.object.release_level,
                    serial=serializer.object.serial
                )
            except DocumentVersion.DoesNotExist:
                self.object = serializer.save(force_insert=True)
            else:
                return Response(
                    {'non_field_errors': 'A version with the same major, minor, micro, release_level and serial values already exist for this document.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIDocumentVersionView(generics.RetrieveAPIView):
    """
    Returns the selected document version details.
    """

    allowed_methods = ['GET']
    serializer_class = DocumentVersionSerializer
    queryset = DocumentVersion.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}
    mayan_permission_attribute_check = 'document'


class APIDocumentImageView(generics.GenericAPIView):
    """
    Returns an image representation of the selected document.
    size -- 'x' seprated width and height of the desired image representation.
    page -- Page number of the document to be imaged.
    zoom -- Zoom level of the image to be generated, numeric value only.
    version -- Version number of the document to be imaged.
    """
    serializer_class = DocumentImageSerializer

    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, request.user, document)

        size = request.GET.get('size', DISPLAY_SIZE)

        page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))

        zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

        version = int(request.GET.get('version', document.latest_version.pk))

        if request.GET.get('as_base64', False):
            base64_version = True

        if zoom < ZOOM_MIN_LEVEL:
            zoom = ZOOM_MIN_LEVEL

        if zoom > ZOOM_MAX_LEVEL:
            zoom = ZOOM_MAX_LEVEL

        rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

        try:
            task = task_get_document_image.apply_async(kwargs=dict(document_id=document.pk, size=size, page=page, zoom=zoom, rotation=rotation, as_base64=True, version=version), queue='converter')
            return Response({
                'status': 'success',
                'data': task.get(timeout=DOCUMENT_IMAGE_TASK_TIMEOUT)
            })
        except UnknownFileFormat as exception:
            return Response({'status': 'error', 'detail': 'unknown_file_format', 'message': unicode(exception)})
        except UnkownConvertError as exception:
            return Response({'status': 'error', 'detail': 'converter_error', 'message': unicode(exception)})


class APIDocumentPageView(generics.RetrieveUpdateAPIView):
    """
    Returns the selected document page details.
    """

    serializer_class = DocumentPageSerializer
    queryset = DocumentPage.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_DOCUMENT_VIEW],
        'PUT': [PERMISSION_DOCUMENT_EDIT],
        'PATCH': [PERMISSION_DOCUMENT_EDIT]
    }
    mayan_permission_attribute_check = 'document'


class APIDocumentTypeListView(generics.ListCreateAPIView):
    """
    Returns a list of all the document types.
    """

    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_TYPE_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_TYPE_CREATE]}


class APIDocumentTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document type details.
    """

    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_DOCUMENT_TYPE_VIEW],
        'PUT': [PERMISSION_DOCUMENT_TYPE_EDIT],
        'PATCH': [PERMISSION_DOCUMENT_TYPE_EDIT],
        'DELETE': [PERMISSION_DOCUMENT_TYPE_DELETE]
    }


class APIDocumentTypeDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents of a particular document type.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_VIEW, self.request.user, document_type)

        return document_type.documents.all()
