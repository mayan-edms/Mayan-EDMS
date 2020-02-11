from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from mayan.apps.permissions.classes import Permission
from mayan.apps.rest_api import generics

from .literals import STAGING_FILE_IMAGE_TASK_TIMEOUT
from .models import StagingFolderSource
from .permissions import permission_staging_file_delete
from .serializers import StagingFolderFileSerializer, StagingFolderSerializer
from .storages import storage_staging_file_image_cache
from .tasks import task_generate_staging_file_image


class APIStagingSourceFileView(generics.RetrieveDestroyAPIView):
    """
    get: Details of the selected staging file.
    """
    serializer_class = StagingFolderFileSerializer

    def get_object(self):
        if self.request.method == 'DELETE':
            Permission.check_user_permissions(
                permissions=(permission_staging_file_delete,),
                user=self.request.user
            )

        staging_folder = get_object_or_404(
            klass=StagingFolderSource, pk=self.kwargs['staging_folder_pk']
        )
        return staging_folder.get_file(
            encoded_filename=self.kwargs['encoded_filename']
        )


class APIStagingSourceListView(generics.ListAPIView):
    """
    get: Returns a list of all the staging folders and the files they contain.
    """
    serializer_class = StagingFolderSerializer
    queryset = StagingFolderSource.objects.all()


class APIStagingSourceView(generics.RetrieveAPIView):
    """
    get: Details of the selected staging folders and the files it contains.
    """
    serializer_class = StagingFolderSerializer
    queryset = StagingFolderSource.objects.all()


class APIStagingSourceFileImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document.
    """
    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def retrieve(self, request, *args, **kwargs):
        width = request.GET.get('width')
        height = request.GET.get('height')

        task = task_generate_staging_file_image.apply_async(
            kwargs=dict(
                staging_folder_pk=self.kwargs['staging_folder_pk'],
                encoded_filename=self.kwargs['encoded_filename'],
                width=width, height=height
            )
        )

        cache_filename = task.get(timeout=STAGING_FILE_IMAGE_TASK_TIMEOUT)

        with storage_staging_file_image_cache.open(cache_filename) as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            return response
