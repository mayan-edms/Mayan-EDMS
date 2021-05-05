from django.contrib.auth.models import Group

from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .querysets import get_user_queryset
from .serializers import (
    GroupSerializer, GroupUserAddSerializer, GroupUserRemoveSerializer,
    UserSerializer
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


class APIGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected group.
    get: Return the details of the selected group.
    patch: Partially edit the selected group.
    put: Edit the selected group.
    """
    lookup_url_kwarg = 'group_id'
    mayan_object_permissions = {
        'GET': (permission_group_view,),
        'PUT': (permission_group_edit,),
        'PATCH': (permission_group_edit,),
        'DELETE': (permission_group_delete,)
    }
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIGroupListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the groups.
    post: Create a new group.
    """
    mayan_object_permissions = {'GET': (permission_group_view,)}
    mayan_view_permissions = {'POST': (permission_group_create,)}
    ordering_fields = ('name',)
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIGroupUserAddView(generics.ObjectActionAPIView):
    """
    post: Add a user to a group.
    """
    lookup_url_kwarg = 'group_id'
    mayan_object_permissions = {
        'POST': (permission_group_edit,)
    }
    serializer_class = GroupUserAddSerializer
    queryset = Group.objects.all()

    def object_action(self, request, serializer):
        self.object._event_actor = self.request.user

        self.object.users_add(
            queryset=get_user_queryset().filter(
                pk=serializer.validated_data['user'].pk
            )
        )


class APIGroupUserListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    Returns a list of all the users belonging to the group.
    """
    external_object_queryset = Group.objects.all()
    external_object_pk_url_kwarg = 'group_id'
    mayan_external_object_permissions = {'GET': (permission_group_view,)}
    mayan_object_permissions = {'GET': (permission_user_view,)}
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.external_object.user_set.all()


class APIGroupUserRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a user from a group.
    """
    lookup_url_kwarg = 'group_id'
    mayan_object_permissions = {
        'POST': (permission_group_edit,)
    }
    serializer_class = GroupUserRemoveSerializer
    queryset = Group.objects.all()

    def object_action(self, request, serializer):
        self.object._event_actor = self.request.user

        self.object.users_remove(
            queryset=get_user_queryset().filter(
                pk=serializer.validated_data['user'].pk
            )
        )


class APIUserListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the users.
    post: Create a new user.
    """
    mayan_object_permissions = {'GET': (permission_user_view,)}
    mayan_view_permissions = {'POST': (permission_user_create,)}
    ordering_fields = (
        'email', 'first_name', 'last_name', 'has_usable_password',
        'is_active', 'username'
    )
    queryset = get_user_queryset()
    serializer_class = UserSerializer

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class APIUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected user.
    get: Return the details of the selected user.
    patch: Partially edit the selected user.
    put: Edit the selected user.
    """
    lookup_url_kwarg = 'user_id'
    mayan_object_permissions = {
        'GET': (permission_user_view,),
        'PUT': (permission_user_edit,),
        'PATCH': (permission_user_edit,),
        'DELETE': (permission_user_delete,)
    }
    queryset = get_user_queryset()
    serializer_class = UserSerializer

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class APIUserGroupListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    Returns a list of all the groups to which the user belongings.
    """
    external_object_queryset = get_user_queryset()
    external_object_pk_url_kwarg = 'user_id'
    mayan_external_object_permissions = {'GET': (permission_user_view,)}
    mayan_object_permissions = {'GET': (permission_group_view,)}
    serializer_class = GroupSerializer

    def get_queryset(self):
        return self.external_object.groups.all()
