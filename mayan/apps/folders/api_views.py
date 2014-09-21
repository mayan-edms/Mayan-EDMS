from __future__ import absolute_import

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Folder
from .permissions import (PERMISSION_FOLDER_CREATE,
                          PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT,
                          PERMISSION_FOLDER_VIEW)
from .serializers import FolderSerializer


class APIFolderListView(generics.ListCreateAPIView):
    """
    Returns a list of all the folders.
    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_FOLDER_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_FOLDER_CREATE]}


class APIFolderView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected folder details.
    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_FOLDER_VIEW],
        'PUT': [PERMISSION_FOLDER_EDIT],
        'PATCH': [PERMISSION_FOLDER_EDIT],
        'DELETE': [PERMISSION_FOLDER_DELETE]
    }
