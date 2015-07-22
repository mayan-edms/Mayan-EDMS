from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from converter.exceptions import UnkownConvertError, UnknownFileFormat
from converter.models import Transformation
from rest_framework import generics
from rest_framework.response import Response

from documents.settings import setting_display_size

from .models import StagingFolderSource
from .serializers import (
    StagingFolderFileSerializer,
    StagingFolderSerializer, StagingSourceFileImageSerializer
)


class APIStagingSourceFileView(generics.GenericAPIView):
    """
    Details of the selected staging file.
    """
    serializer_class = StagingFolderFileSerializer

    def get(self, request, staging_folder_pk, encoded_filename):
        staging_folder = get_object_or_404(
            StagingFolderSource, pk=staging_folder_pk
        )
        return Response(
            StagingFolderFileSerializer(
                staging_folder.get_file(encoded_filename=encoded_filename),
                context={'request': request}
            ).data
        )


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
        staging_folder = get_object_or_404(
            StagingFolderSource, pk=staging_folder_pk
        )
        staging_file = staging_folder.get_file(
            encoded_filename=encoded_filename
        )

        size = request.GET.get('size', setting_display_size.value)

        try:
            return Response({
                'status': 'success',
                'data': staging_file.get_image(
                    as_base64=True, size=size,
                    transformations=Transformation.objects.get_for_model(
                        staging_folder, as_classes=True
                    )
                )
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
