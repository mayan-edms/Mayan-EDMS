from __future__ import absolute_import

import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response

from acls.models import AccessEntry
from converter.exceptions import UnknownFileFormat, UnkownConvertError
from converter.literals import (DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION,
    DEFAULT_PAGE_NUMBER)
from permissions.models import Permission

from .conf.settings import DISPLAY_SIZE, ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL
from .models import Document, DocumentVersion, DocumentPage
from .permissions import PERMISSION_DOCUMENT_VIEW
from .serializers import (DocumentImageSerializer, DocumentPageSerializer,
    DocumentSerializer, DocumentVersionSerializer)

logger = logging.getLogger(__name__)

# API Views


class APIDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class APIDocumentPageView(generics.RetrieveAPIView):
    """
    Returns the selected document page details.
    """

    allowed_methods = ['GET']
    serializer_class = DocumentPageSerializer
    queryset = DocumentPage.objects.all()


class APIDocumentView(generics.RetrieveAPIView):
    """
    Returns the selected document details.
    """

    allowed_methods = ['GET']
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class APIDocumentVersionView(generics.RetrieveAPIView):
    """
    Returns the selected document version details.
    """

    allowed_methods = ['GET']
    serializer_class = DocumentVersionSerializer
    queryset = DocumentVersion.objects.all()


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

        logger.debug('document: %s' % document)

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
            return Response({'status': 'success',
                'data': document.get_image(size=size, page=page, zoom=zoom, rotation=rotation, as_base64=True, version=version)
                })
        except UnknownFileFormat as exception:
            return Response({'status': 'error', 'detail': 'unknown_file_format', 'message': unicode(exception)})
        except UnkownConvertError as exception:
            return Response({'status': 'error', 'detail': 'converter_error', 'message': unicode(exception)})
