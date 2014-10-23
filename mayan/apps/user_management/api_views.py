from __future__ import absolute_import

from django.contrib.auth.models import User

from rest_framework import generics, views
from rest_framework.response import Response

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import (PERMISSION_USER_CREATE, PERMISSION_USER_DELETE,
                          PERMISSION_USER_EDIT, PERMISSION_USER_VIEW)
from .serializers import UserSerializer


class APIUserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_USER_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_USER_CREATE]}

    def get(self, *args, **kwargs):
        """Returns a list of all the users."""
        return super(APIUserListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new user."""
        return super(APIUserListView, self).post(*args, **kwargs)


class APIUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_USER_VIEW],
        'PUT': [PERMISSION_USER_EDIT],
        'PATCH': [PERMISSION_USER_EDIT],
        'DELETE': [PERMISSION_USER_DELETE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected user."""
        return super(APIUserView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected user."""
        return super(APIUserView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected user."""
        return super(APIUserView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected user."""
        return super(APIUserView, self).put(*args, **kwargs)


class APICurrentUserView(views.APIView):
    def get(self, request):
        """Return the details of the current user."""

        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
