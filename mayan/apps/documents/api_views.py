from __future__ import absolute_import, unicode_literals

# TODO: Improve API methods docstrings
import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessControlList
from common.models import SharedUploadedFile
from converter.exceptions import UnkownConvertError, UnknownFileFormat
from converter.literals import (
    DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
)
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from .models import (
    Document, DocumentPage, DocumentType, DocumentVersion, RecentDocument
)
from .permissions import (
    permission_document_create, permission_document_delete,
    permission_document_edit, permission_document_new_version,
    permission_document_properties_edit, permission_document_view,
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view
)
from .serializers import (
    DocumentImageSerializer, DocumentPageSerializer, DocumentSerializer,
    DocumentTypeSerializer, DocumentVersionSerializer, NewDocumentSerializer,
    RecentDocumentSerializer
)
from .settings import (
    setting_display_size, setting_language, setting_zoom_max_level,
    setting_zoom_min_level
)
from .tasks import task_get_document_page_image, task_upload_new_version

logger = logging.getLogger(__name__)


class APIDocumentListView(generics.ListCreateAPIView):
    """
    Returns a list of all the documents.
    """

    queryset = Document.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_document_view],
                                'POST': [permission_document_create]}

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        elif self.request.method == 'POST':
            return NewDocumentSerializer

    def post(self, *args, **kwargs):
        """Create a new document."""
        return super(APIDocumentListView, self).post(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES
        )

        if serializer.is_valid():
            document_type = get_object_or_404(
                DocumentType, pk=serializer.data['document_type']
            )

            logger.info(
                'Creating document version for document type: %s', document_type
            )

            document = Document.objects.create(
                description=serializer.data['description'] or '',
                document_type=document_type,
                label=serializer.data['label'] or serializer.data['file'],
                language=serializer.data['language'] or setting_language.value
            )
            document.save(_user=request.user)

            shared_uploaded_file = SharedUploadedFile.objects.create(
                file=request.FILES['file']
            )

            task_upload_new_version.delay(
                shared_uploaded_file_id=shared_uploaded_file.pk,
                document_id=document.pk, user_id=request.user.pk,
            )

            logger.info(
                'New document version queued for document: %s', document
            )

            serializer.object = document

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIDocumentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document details.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [permission_document_view],
        'PUT': [permission_document_properties_edit],
        'PATCH': [permission_document_properties_edit],
        'DELETE': [permission_document_delete]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected document."""
        return super(APIDocumentView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected document."""
        return super(APIDocumentView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the properties of the selected document."""
        return super(APIDocumentView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the properties of the selected document."""
        return super(APIDocumentView, self).put(*args, **kwargs)


class APIDocumentVersionCreateView(generics.CreateAPIView):
    """
    Create a new document version.
    """

    serializer_class = DocumentVersionSerializer
    queryset = DocumentVersion.objects.all()

    permission_classes = (MayanPermission,)
    mayan_view_permissions = {'POST': [permission_document_new_version]}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES
        )

        if serializer.is_valid():
            # Nested resource we take the document pk from the URL and insert
            # it so that it needs not to be specified by the user, we mark
            # it as a read only field in the serializer
            document = get_object_or_404(Document, pk=kwargs['pk'])

            document.new_version(
                file_object=serializer.object.file,
                comment=serializer.object.comment, _user=request.user
            )

            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_202_ACCEPTED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIDocumentVersionView(generics.RetrieveAPIView):
    """
    Returns the selected document version details.
    """

    allowed_methods = ['GET']
    serializer_class = DocumentVersionSerializer
    queryset = DocumentVersion.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {'GET': [permission_document_view]}
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
            Permission.check_permissions(
                request.user, [permission_document_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, document
            )

        size = request.GET.get('size', setting_display_size.value)

        page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))

        zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

        version = int(request.GET.get('version', document.latest_version.pk))

        if zoom < setting_zoom_min_level.value:
            zoom = setting_zoom_min_level.value

        if zoom > setting_zoom_max_level.value:
            zoom = setting_zoom_max_level.value

        rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

        document_page = document.pages.get(page_number=page)

        try:
            task = task_get_document_page_image.apply_async(
                kwargs=dict(
                    document_page_id=document_page.pk, size=size, zoom=zoom,
                    rotation=rotation, as_base64=True, version=version
                )
            )
            # TODO: prepend 'data:%s;base64,%s' based on format specified in
            # async call
            return Response({
                'status': 'success',
                'data': task.get(timeout=DOCUMENT_IMAGE_TASK_TIMEOUT)
            })
        except UnknownFileFormat as exception:
            return Response(
                {
                    'status': 'error', 'detail': 'unknown_file_format',
                    'message': unicode(exception)
                }
            )
        except UnkownConvertError as exception:
            return Response(
                {
                    'status': 'error', 'detail': 'converter_error',
                    'message': unicode(exception)
                }
            )


class APIDocumentPageView(generics.RetrieveUpdateAPIView):
    """
    Returns the selected document page details.
    """

    serializer_class = DocumentPageSerializer
    queryset = DocumentPage.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [permission_document_view],
        'PUT': [permission_document_edit],
        'PATCH': [permission_document_edit]
    }
    mayan_permission_attribute_check = 'document'

    def get(self, *args, **kwargs):
        """Returns the selected document page details."""
        return super(APIDocumentPageView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected document page."""
        return super(APIDocumentPageView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected document page."""
        return super(APIDocumentPageView, self).put(*args, **kwargs)


class APIDocumentTypeListView(generics.ListCreateAPIView):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_document_type_view]}
    mayan_view_permissions = {'POST': [permission_document_type_create]}

    def get(self, *args, **kwargs):
        """Returns a list of all the document types."""
        return super(APIDocumentTypeListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new document type."""
        return super(APIDocumentTypeListView, self).post(*args, **kwargs)


class APIDocumentTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document type details.
    """

    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [permission_document_type_view],
        'PUT': [permission_document_type_edit],
        'PATCH': [permission_document_type_edit],
        'DELETE': [permission_document_type_delete]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected document type."""
        return super(APIDocumentTypeView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected document type."""
        return super(APIDocumentTypeView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the properties of the selected document type."""
        return super(APIDocumentTypeView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the properties of the selected document type."""
        return super(APIDocumentTypeView, self).put(*args, **kwargs)


class APIDocumentTypeDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents of a particular document type.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_document_view]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, [permission_document_type_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_type_view, self.request.user,
                document_type
            )

        return document_type.documents.all()


class APIRecentDocumentListView(generics.ListAPIView):
    serializer_class = RecentDocumentSerializer

    def get_queryset(self):
        return RecentDocument.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        """Return a list of the recent documents for the current user."""
        return super(APIRecentDocumentListView, self).get(*args, **kwargs)
