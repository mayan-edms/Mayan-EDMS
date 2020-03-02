from __future__ import unicode_literals

from django.contrib.auth.models import Group

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mayan.apps.rest_api import generics, viewsets

from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .querysets import get_user_queryset
from .serializers import (
    GroupSerializer, GroupUserAddRemoveSerializer,
    UserGroupAddRemoveSerializer, UserSerializer
)


class CurrentUserAPIView(generics.RetrieveUpdateAPIView):
    """
    get: Return the details of the current user.
    patch: Partially edit the current user.
    put: Edit the current user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class GroupAPIViewSet(viewsets.MayanModelAPIViewSet):
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
        operation_description='Delete the selected group.'
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
            data=serializer.data, headers=headers, status=status.HTTP_200_OK
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

        return Response(data=serializer.data)

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
            data=serializer.data, headers=headers, status=status.HTTP_200_OK
        )


class UserAPIViewSet(viewsets.MayanModelAPIViewSet):
    lookup_url_kwarg = 'user_id'
    object_permission_map = {
        'destroy': permission_user_delete,
        'group_add': permission_user_edit,
        'group_list': permission_user_view,
        'group_remove': permission_user_edit,
        'list': permission_user_view,
        'partial_update': permission_user_edit,
        'retrieve': permission_user_view,
        'update': permission_user_edit,
    }
    queryset = get_user_queryset()
    serializer_class = UserSerializer
    view_permission_map = {
        'create': permission_user_create
    }

    @swagger_auto_schema(
        operation_description='Create a new user.'
    )
    def create(self, *args, **kwargs):
        return super(UserAPIViewSet, self).create(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Delete the selected user.'
    )
    def destroy(self, *args, **kwargs):
        return super(UserAPIViewSet, self).destroy(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve the list of all the users.',
    )
    def list(self, *args, **kwargs):
        return super(UserAPIViewSet, self).list(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update the selected user.',
    )
    def partial_update(self, *args, **kwargs):
        return super(UserAPIViewSet, self).partial_update(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve the details of the selected user.',
    )
    def retrieve(self, *args, **kwargs):
        return super(UserAPIViewSet, self).retrieve(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Update the selected user.',
    )
    def update(self, *args, **kwargs):
        return super(UserAPIViewSet, self).update(*args, **kwargs)

    @swagger_auto_schema(
        operation_description='Add the selected user to a group.',
        responses={
            200: '',
        }
    )
    @action(
        detail=True, lookup_url_kwarg='user_id', methods=('post',),
        serializer_class=UserGroupAddRemoveSerializer,
        url_name='group-add', url_path='groups/add'
    )
    def group_add(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.groups_add(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            data=serializer.data, headers=headers, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description=(
            'Retrieve the list of groups to which the selected '
            'user belongs to.'
        )
    )
    @action(
        detail=True, lookup_url_kwarg='user_id',
        serializer_class=GroupSerializer, url_name='group-list',
        url_path='groups'
    )
    def group_list(self, request, *args, **kwargs):
        queryset = self.get_object().get_groups(user=self.request.user)
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(
            instance=queryset, context={'request': request}, many=True
        )

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Remove the selected user from a group.',
        responses={
            200: '',
        }
    )
    @action(
        detail=True, lookup_url_kwarg='user_id',
        methods=('post',), serializer_class=UserGroupAddRemoveSerializer,
        url_name='group-remove', url_path='groups/remove'
    )
    def group_remove(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.groups_remove(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            data=serializer.data, headers=headers, status=status.HTTP_200_OK
        )
