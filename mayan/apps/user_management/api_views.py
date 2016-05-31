from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import MayanGroup
from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .serializers import GroupSerializer, UserSerializer


class APIGroupListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_group_view,)}
    mayan_view_permissions = {'POST': (permission_group_create,)}
    permission_classes = (MayanPermission,)
    queryset = MayanGroup.on_organization.all()
    serializer_class = GroupSerializer

    def get(self, *args, **kwargs):
        """
        Returns a list of all the groups.
        """

        return super(APIGroupListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new group.
        """

        return super(APIGroupListView, self).post(*args, **kwargs)


class APIGroupView(generics.RetrieveUpdateDestroyAPIView):
    mayan_object_permissions = {
        'GET': (permission_group_view,),
        'PUT': (permission_group_edit,),
        'PATCH': (permission_group_edit,),
        'DELETE': (permission_group_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = MayanGroup.on_organization.all()
    serializer_class = GroupSerializer

    def delete(self, *args, **kwargs):
        """
        Delete the selected group.
        """

        return super(APIGroupView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected group.
        """

        return super(APIGroupView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Partially edit the selected group.
        """

        return super(APIGroupView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected group.
        """

        return super(APIGroupView, self).put(*args, **kwargs)


class APIUserListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_user_view,)}
    mayan_view_permissions = {'POST': (permission_user_create,)}
    permission_classes = (MayanPermission,)
    queryset = get_user_model().on_organization.all()
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        """
        Returns a list of all the users.
        """
        return super(APIUserListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new user.
        """

        return super(APIUserListView, self).post(*args, **kwargs)


class APIUserView(generics.RetrieveUpdateDestroyAPIView):
    mayan_object_permissions = {
        'GET': (permission_user_view,),
        'PUT': (permission_user_edit,),
        'PATCH': (permission_user_edit,),
        'DELETE': (permission_user_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = get_user_model().on_organization.all()
    serializer_class = UserSerializer

    def delete(self, *args, **kwargs):
        """
        Delete the selected user.
        """

        return super(APIUserView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected user.
        """

        return super(APIUserView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Partially edit the selected user.
        """

        return super(APIUserView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected user.
        """

        return super(APIUserView, self).put(*args, **kwargs)


class APICurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, *args, **kwargs):
        """
        Delete the current user.
        """

        return super(APICurrentUserView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the current user.
        """

        return super(APICurrentUserView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Partially edit the current user.
        """

        return super(APICurrentUserView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the current user.
        """

        return super(APICurrentUserView, self).put(*args, **kwargs)
