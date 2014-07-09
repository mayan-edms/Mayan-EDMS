from __future__ import absolute_import

import logging

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response

from converter.exceptions import UnkownConvertError, UnknownFileFormat
from converter.literals import DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
from documents.conf.settings import DISPLAY_SIZE, ZOOM_MAX_LEVEL, ZOOM_MIN_LEVEL

from .models import StagingFolder
from .serializers import SerializerStagingFolder, SerializerStagingFolderFile

logger = logging.getLogger(__name__)

# API Views


class APIStagingSourceFileView(generics.GenericAPIView):
    """
    Details of the selected staging file.
    """
    def get(self, request, staging_folder_pk, filename):
        staging_folder = get_object_or_404(StagingFolder, pk=staging_folder_pk)
        return Response(SerializerStagingFolderFile(staging_folder.get_file(encoded_filename=filename), context={'request': request}).data)


class APIStagingSourceListView(generics.ListAPIView):
    """
    Returns a list of all the staging folders and the files they contain.
    """

    serializer_class = SerializerStagingFolder
    queryset = StagingFolder.objects.all()


class APIStagingSourceView(generics.RetrieveAPIView):
    """
    Details of the selected staging folders and the files it contains.
    """
    serializer_class = SerializerStagingFolder
    queryset = StagingFolder.objects.all()


class APIStagingSourceFileImageView(generics.GenericAPIView):
    """
    Image of the selected staging file.
    """
    def get(self, request, staging_folder_pk, filename):
        staging_folder = get_object_or_404(StagingFolder, pk=staging_folder_pk)
        staging_file = staging_folder.get_file(encoded_filename=filename)

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
            return Response({'status': 'success',
                'data': staging_file.get_image(size=size, page=page, zoom=zoom, rotation=rotation, as_base64=True)
                })
        except UnknownFileFormat as exception:
            return Response({'status': 'error', 'detail': 'unknown_file_format', 'message': unicode(exception)})
        except UnkownConvertError as exception:
            return Response({'status': 'error', 'detail': 'converter_error', 'message': unicode(exception)})

