from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.viewsets import MayanModelAPIViewSet

from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .serializers import (
    GroupSerializer, GroupUserAddRemoveSerializer, UserSerializer,
    UserGroupListSerializer
)


class GroupAPIViewSet(MayanModelAPIViewSet):
    lookup_url_kwarg = 'group_id'
    object_permission_map = {
        'destroy': permission_group_delete,
        'list': permission_group_view,
        'partial_update': permission_group_edit,
        'retrieve': permission_group_view,
        'update': permission_group_edit,
        'user_add': permission_group_edit,
        'user_list': permission_group_view,
        'user_remove': permission_group_edit
    }
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    view_permission_map = {
        'create': permission_group_create
    }

    @swagger_auto_schema(
        operation_description='Create a new group.'
    )
    def create(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).create(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Delete the selected group.', responses={
            204: '',
        }
    )
    def destroy(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).destroy(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve the list of all the groups.',
    )
    def list(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).list(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update the selected group.',
    )
    def partial_update(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).partial_update(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve the details of the selected group.',
    )
    def retrieve(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).retrieve(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update the selected group.',
    )
    def update(self, *args, **kwargs):
        return super(GroupAPIViewSet, self).update(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Add a user to the selected group.', responses={
            200: '',
        }
    )
    @action(
        detail=True, lookup_url_kwarg='group_id', methods=('post',),
        serializer_class=GroupUserAddRemoveSerializer,
        url_name='user-add', url_path='users/add'
    )
    def user_add(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.users_add(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @swagger_auto_schema(
        operation_description='Retrieve the list of users in the selected group.'
    )
    @action(
        detail=True, lookup_url_kwarg='group_id',
        serializer_class=UserSerializer, url_name='user-list',
        url_path='users'
    )
    def user_list(self, request, *args, **kwargs):
        queryset = self.get_object().get_users(user=self.request.user)
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Remove a user to the selected group.',
        responses={
            200: '',
        }
    )
    @action(
        detail=True, lookup_url_kwarg='group_id',
        methods=('post',), serializer_class=GroupUserAddRemoveSerializer,
        url_name='user-remove', url_path='users/remove'
    )
    def user_remove(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.users_remove(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
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


class APIUserListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the users.
    post: Create a new user.
    """
    mayan_object_permissions = {'GET': (permission_user_view,)}
    mayan_view_permissions = {'POST': (permission_user_create,)}
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
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class APIUserGroupList(generics.ListCreateAPIView):
    """
    get: Returns a list of all the groups to which a user belongs.
    post: Add a user to a list of groups.
    """
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

        return AccessControlList.objects.restrict_queryset(
            permission=permission_group_view,
            queryset=user.groups.order_by('id'), user=self.request.user
        )

    def get_user(self):
        if self.request.method == 'GET':
            permission = permission_user_view
        else:
            permission = permission_user_edit

        user = get_object_or_404(klass=get_user_model(), pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=user, permissions=(permission,), user=self.request.user
        )
        return user

    def perform_create(self, serializer):
        serializer.save(user=self.get_user(), _user=self.request.user)
