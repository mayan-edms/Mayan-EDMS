from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessControlList
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .serializers import (
    GroupSerializer, UserSerializer, UserGroupListSerializer
)


class APICurrentUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the current user.
    get: Return the details of the current user.
    patch: Partially edit the current user.
    put: Edit the current user.
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class APIGroupListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the groups.
    post: Create a new group.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_group_view,)}
    mayan_view_permissions = {'POST': (permission_group_create,)}
    permission_classes = (MayanPermission,)
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer


class APIGroupView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected group.
    get: Return the details of the selected group.
    patch: Partially edit the selected group.
    put: Edit the selected group.
    """
    mayan_object_permissions = {
        'GET': (permission_group_view,),
        'PUT': (permission_group_edit,),
        'PATCH': (permission_group_edit,),
        'DELETE': (permission_group_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer


class APIUserListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the users.
    post: Create a new user.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_user_view,)}
    mayan_view_permissions = {'POST': (permission_user_create,)}
    permission_classes = (MayanPermission,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class APIUserView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected user.
    get: Return the details of the selected user.
    patch: Partially edit the selected user.
    put: Edit the selected user.
    """
    mayan_object_permissions = {
        'GET': (permission_user_view,),
        'PUT': (permission_user_edit,),
        'PATCH': (permission_user_edit,),
        'DELETE': (permission_user_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class APIUserGroupList(generics.ListCreateAPIView):
    """
    get: Returns a list of all the groups to which an user belongs.
    post: Add a user to a list of groups.
    """
    mayan_object_permissions = {
        'GET': (permission_user_view,),
        'POST': (permission_user_edit,)
    }
    permission_classes = (MayanPermission,)

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIUserGroupList, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupSerializer
        elif self.request.method == 'POST':
            return UserGroupListSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIUserGroupList, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'user': self.get_user(),
                }
            )

        return context

    def get_queryset(self):
        user = self.get_user()

        return AccessControlList.objects.filter_by_access(
            permission_group_view, self.request.user,
            queryset=user.groups.order_by('id')
        )

    def get_user(self):
        if self.request.method == 'GET':
            permission = permission_user_view
        else:
            permission = permission_user_edit

        user = get_object_or_404(get_user_model(), pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=(permission,), user=self.request.user,
            obj=user
        )
        return user

    def perform_create(self, serializer):
        serializer.save(user=self.get_user(), _user=self.request.user)
