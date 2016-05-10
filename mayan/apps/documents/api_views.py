from __future__ import absolute_import, unicode_literals

import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from filetransfers.api import serve_file
from rest_framework import generics, status
from rest_framework.response import Response

from acls.models import AccessControlList
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import (
    Document, DocumentPage, DocumentType, DocumentVersion, RecentDocument
)
from .permissions import (
    permission_document_create, permission_document_delete,
    permission_document_download, permission_document_edit,
    permission_document_new_version, permission_document_properties_edit,
    permission_document_restore, permission_document_trash,
    permission_document_version_revert, permission_document_view,
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view
)
from .serializers import (
    DeletedDocumentSerializer, DocumentPageImageSerializer,
    DocumentPageSerializer, DocumentSerializer,
    DocumentTypeSerializer, DocumentVersionSerializer,
    DocumentVersionRevertSerializer, NewDocumentSerializer,
    NewDocumentVersionSerializer, RecentDocumentSerializer
)

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
    """

    mayan_object_permissions = {
        'DELETE': (permission_document_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.trash.all()
    serializer_class = DeletedDocumentSerializer

    def delete(self, *args, **kwargs):
        """
        Delete the trashed document.
        """

        return super(APIDeletedDocumentView, self).delete(*args, **kwargs)


class APIDeletedDocumentRestoreView(generics.GenericAPIView):
    """
    Restore a trashed document.
    """

    mayan_object_permissions = {
        'POST': (permission_document_restore,)
    }

    permission_classes = (MayanPermission,)
    queryset = Document.trash.all()
    serializer_class = DeletedDocumentSerializer

    def post(self, *args, **kwargs):
        self.get_object().restore()
        return Response(status=status.HTTP_200_OK)


class APIDocumentDownloadView(generics.RetrieveAPIView):
    """
    Download the latest version of a document.
    ---
    GET:
        omit_serializer: true
        parameters:
            - name: pk
              paramType: path
              type: number
    """

    mayan_object_permissions = {
        'GET': (permission_document_download,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()

    def get_serializer_class(self):
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return serve_file(
            request,
            instance.latest_version.file,
            save_as='"%s"' % instance.label,
            content_type=instance.latest_version.mimetype if instance.latest_version.mimetype else 'application/octet-stream'
        )


class APIDocumentListView(generics.ListCreateAPIView):
    """
    Returns a list of all the documents.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    mayan_view_permissions = {'POST': (permission_document_create,)}
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        elif self.request.method == 'POST':
            return NewDocumentSerializer

    def perform_create(self, serializer):
        serializer.save(_user=self.request.user)

    def post(self, *args, **kwargs):
        """
        Create a new document.
        """

        return super(APIDocumentListView, self).post(*args, **kwargs)


class APIDocumentVersionDownloadView(generics.RetrieveAPIView):
    """
    Download a document version.
    ---
    GET:
        omit_serializer: true
        parameters:
            - name: pk
              paramType: path
              type: number
    """

    mayan_object_permissions = {
        'GET': (permission_document_download,)
    }
    permission_classes = (MayanPermission,)
    queryset = DocumentVersion.objects.all()

    def get_serializer_class(self):
        return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return serve_file(
            request,
            instance.file,
            save_as='"%s"' % instance.document.label,
            content_type=instance.mimetype if instance.mimetype else 'application/octet-stream'
        )


class APIDocumentView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document details.
    """

    mayan_object_permissions = {
        'GET': (permission_document_view,),
        'PUT': (permission_document_properties_edit,),
        'PATCH': (permission_document_properties_edit,),
        'DELETE': (permission_document_trash,)
    }
    permission_classes = (MayanPermission,)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def delete(self, *args, **kwargs):
        """
        Move the selected document to the thrash.
        """

        return super(APIDocumentView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected document.
        """

        return super(APIDocumentView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the properties of the selected document.
        """

        return super(APIDocumentView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the properties of the selected document.
        """

        return super(APIDocumentView, self).put(*args, **kwargs)


class APIDocumentPageImageView(generics.RetrieveAPIView):
    """
    Returns an image representation of the selected document.
    size -- 'x' seprated width and height of the desired image representation.
    zoom -- Zoom level of the image to be generated, numeric value only.
    """

    mayan_object_permissions = {
        'GET': (permission_document_view,),
    }
    mayan_permission_attribute_check = 'document'
    permission_classes = (MayanPermission,)
    queryset = DocumentPage.objects.all()
    serializer_class = DocumentPageImageSerializer


class APIDocumentPageView(generics.RetrieveUpdateAPIView):
    """
    Returns the selected document page details.
    """

    mayan_object_permissions = {
        'GET': (permission_document_view,),
        'PUT': (permission_document_edit,),
        'PATCH': (permission_document_edit,)
    }
    mayan_permission_attribute_check = 'document'
    permission_classes = (MayanPermission,)
    queryset = DocumentPage.objects.all()
    serializer_class = DocumentPageSerializer

    def get(self, *args, **kwargs):
        """
        Returns the selected document page details.
        """

        return super(APIDocumentPageView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the selected document page.
        """

        return super(APIDocumentPageView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected document page.
        """

        return super(APIDocumentPageView, self).put(*args, **kwargs)


class APIDocumentTypeListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_type_view,)}
    mayan_view_permissions = {'POST': (permission_document_type_create,)}
    permission_classes = (MayanPermission,)
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def get(self, *args, **kwargs):
        """
        Returns a list of all the document types.
        """

        return super(APIDocumentTypeListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new document type.
        """

        return super(APIDocumentTypeListView, self).post(*args, **kwargs)


class APIDocumentTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document type details.
    """

    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
        'PUT': (permission_document_type_edit,),
        'PATCH': (permission_document_type_edit,),
        'DELETE': (permission_document_type_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def delete(self, *args, **kwargs):
        """
        Delete the selected document type.
        """

        return super(APIDocumentTypeView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected document type.
        """

        return super(APIDocumentTypeView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the properties of the selected document type.
        """

        return super(APIDocumentTypeView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the properties of the selected document type.
        """

        return super(APIDocumentTypeView, self).put(*args, **kwargs)


class APIDocumentTypeDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents of a particular document type.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, (permission_document_type_view,)
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
        """
        Return a list of the recent documents for the current user.
        """

        return super(APIRecentDocumentListView, self).get(*args, **kwargs)


class APIDocumentVersionsListView(generics.ListCreateAPIView):
    """
    Return a list of the selected document's versions.
    """

    mayan_object_permissions = {
        'GET': (permission_document_view,),
    }
    mayan_permission_attribute_check = 'document'
    mayan_view_permissions = {'POST': (permission_document_new_version,)}
    permission_classes = (MayanPermission,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentVersionSerializer
        elif self.request.method == 'POST':
            return NewDocumentVersionSerializer

    def get_queryset(self):
        return get_object_or_404(Document, pk=self.kwargs['pk']).versions.all()

    def perform_create(self, serializer):
        serializer.save(
            document=get_object_or_404(Document, pk=self.kwargs['pk']),
            _user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        """
        Create a new document version.
        """

        return super(
            APIDocumentVersionsListView, self
        ).post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_202_ACCEPTED, headers=headers)


class APIDocumentVersionView(generics.RetrieveUpdateAPIView):
    """
    Returns the selected document version details.
    """

    mayan_object_permissions = {
        'GET': (permission_document_view,),
        'PATCH': (permission_document_edit,),
        'PUT': (permission_document_edit,),
    }
    mayan_permission_attribute_check = 'document'
    permission_classes = (MayanPermission,)
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer

    def patch(self, *args, **kwargs):
        """
        Edit the selected document version.
        """

        return super(APIDocumentVersionView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected document version.
        """

        return super(APIDocumentVersionView, self).put(*args, **kwargs)


class APIDocumentVersionRevertView(generics.GenericAPIView):
    """
    Revert to an earlier document version.
    """

    mayan_object_permissions = {
        'POST': (permission_document_version_revert,)
    }
    mayan_permission_attribute_check = 'document'
    permission_classes = (MayanPermission,)
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionRevertSerializer

    def post(self, *args, **kwargs):
        self.get_object().revert(_user=self.request.user)
        return Response(status=status.HTTP_200_OK)
