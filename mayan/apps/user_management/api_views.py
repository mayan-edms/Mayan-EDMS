from __future__ import absolute_import

from django.contrib.auth.models import User

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import (PERMISSION_USER_CREATE,
                          PERMISSION_USER_DELETE, PERMISSION_USER_EDIT,
                          PERMISSION_USER_VIEW)
from .serializers import UserSerializer


class APIUserListView(generics.ListCreateAPIView):
    """
    Returns a list of all the folders.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_USER_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_USER_CREATE]}


class APIUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected folder details.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_USER_VIEW],
        'PUT': [PERMISSION_USER_EDIT],
        'PATCH': [PERMISSION_USER_EDIT],
        'DELETE': [PERMISSION_USER_DELETE]
    }
