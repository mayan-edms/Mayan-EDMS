from __future__ import absolute_import

import tempfile

from django.shortcuts import get_object_or_404

from converter.exceptions import UnkownConvertError, UnknownFileFormat
from converter.literals import (DEFAULT_PAGE_NUMBER,
                                DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL)
from rest_framework import generics
from rest_framework.response import Response

from documents.permissions import PERMISSION_DOCUMENT_CREATE
from documents.settings import (DISPLAY_SIZE, ZOOM_MAX_LEVEL,
                                ZOOM_MIN_LEVEL)
from rest_api.permissions import MayanPermission

from .models import StagingFolderSource, WatchFolderSource
from .serializers import (NewDocumentSerializer, StagingFolderFileSerializer,
                          StagingFolderSerializer,
                          StagingSourceFileImageSerializer,
                          WebFormSourceSerializer)
from .tasks import task_upload_document


class APIStagingSourceFileView(generics.GenericAPIView):
    """
    Details of the selected staging file.
    """
    serializer_class = StagingFolderFileSerializer

    def get(self, request, staging_folder_pk, encoded_filename):
        staging_folder = get_object_or_404(StagingFolderSource, pk=staging_folder_pk)
        return Response(StagingFolderFileSerializer(staging_folder.get_file(encoded_filename=encoded_filename), context={'request': request}).data)


class APIStagingSourceListView(generics.ListAPIView):
    """
    Returns a list of all the staging folders and the files they contain.
    """

    serializer_class = StagingFolderSerializer
    queryset = StagingFolderSource.objects.all()


class APIStagingSourceView(generics.RetrieveAPIView):
    """
    Details of the selected staging folders and the files it contains.
    """
    serializer_class = StagingFolderSerializer
    queryset = StagingFolderSource.objects.all()


class APIStagingSourceFileImageView(generics.GenericAPIView):
    """
    Image of the selected staging file.
    size -- 'x' seprated width and height of the desired image representation.
    page -- Page number of the staging file to be imaged.
    zoom -- Zoom level of the image to be generated, numeric value only.
    """

    serializer_class = StagingSourceFileImageSerializer

    def get(self, request, staging_folder_pk, encoded_filename):
        staging_folder = get_object_or_404(StagingFolderSource, pk=staging_folder_pk)
        staging_file = staging_folder.get_file(encoded_filename=encoded_filename)

        size = request.GET.get('size', DISPLAY_SIZE)

        page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))

        zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

        if request.GET.get('as_base64', False):
            base64_version = True

        if zoom < ZOOM_MIN_LEVEL:
            zoom = ZOOM_MIN_LEVEL

        if zoom > ZOOM_MAX_LEVEL:
            zoom = ZOOM_MAX_LEVEL

        rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

        try:
            return Response({
                'status': 'success',
                'data': staging_file.get_image(size=size, page=page, zoom=zoom, rotation=rotation, as_base64=True)
            })
        except UnknownFileFormat as exception:
            return Response({'status': 'error', 'detail': 'unknown_file_format', 'message': unicode(exception)})
        except UnkownConvertError as exception:
            return Response({'status': 'error', 'detail': 'converter_error', 'message': unicode(exception)})


class APIDocumentCreateView(generics.CreateAPIView):
    """
    Create a new document from an uploaded file.
    """

    serializer_class = NewDocumentSerializer

    permission_classes = (MayanPermission,)
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_CREATE]}

    def get_serializer_class(self):
        return NewDocumentSerializer

    def create(self, request):
        # TODO: use serializer instance instead of raw request
        request = self.request.POST

        if self.request.FILES:
            temporary_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in self.request.FILES['file'].chunks():
                temporary_file.write(chunk)

            temporary_file.close()
        else:
            return Response({
                'status': 'error',
                'message': 'No file provided.'
            })

        if not self.request.user.is_anonymous():
            user_id = self.request.user.pk
        else:
            user_id = None

        task_upload_document.apply_async(kwargs=dict(
            source_id=int(request.get('source')),
            file_path=temporary_file.name, filename=request.get('filename', None),
            use_file_name=request.get('use_file_name', False),
            document_type_id=int(request.get('document_type', 0)) or None,
            expand=request.get('expand', False),
            metadata_dict_list={},
            user_id=user_id,
            description=request.get('description', None),
        ), queue='uploads')

        return Response({
            'status': 'success',
            'message': 'New document creation queued.'
        })
