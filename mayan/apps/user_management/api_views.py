from __future__ import unicode_literals

from django.contrib.auth.models import Group, User

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import (
    PERMISSION_GROUP_CREATE, PERMISSION_GROUP_DELETE, PERMISSION_GROUP_EDIT,
    PERMISSION_GROUP_VIEW, PERMISSION_USER_CREATE, PERMISSION_USER_DELETE,
    PERMISSION_USER_EDIT, PERMISSION_USER_VIEW
)
from .serializers import GroupSerializer, UserSerializer


class APIGroupListView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_GROUP_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_GROUP_CREATE]}

    def get(self, *args, **kwargs):
        """Returns a list of all the groups."""
        return super(APIGroupListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new group."""
        return super(APIGroupListView, self).post(*args, **kwargs)


class APIGroupView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_GROUP_VIEW],
        'PUT': [PERMISSION_GROUP_EDIT],
        'PATCH': [PERMISSION_GROUP_EDIT],
        'DELETE': [PERMISSION_GROUP_DELETE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected group."""
        return super(APIGroupView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected group."""
        return super(APIGroupView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Partially edit the selected group."""
        return super(APIGroupView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected group."""
        return super(APIGroupView, self).put(*args, **kwargs)


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
        """Partially edit the selected user."""
        return super(APIUserView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected user."""
        return super(APIUserView, self).put(*args, **kwargs)


class APICurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, *args, **kwargs):
        """Delete the current user."""
        return super(APICurrentUserView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the current user."""
        return super(APICurrentUserView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Partially edit the current user."""
        return super(APICurrentUserView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the current user."""
        return super(APICurrentUserView, self).put(*args, **kwargs)
