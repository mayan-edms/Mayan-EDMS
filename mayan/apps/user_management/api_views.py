from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)
from .serializers import GroupSerializer, UserSerializer
from rest_framework import authentication, permissions


class APIGroupListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_group_view,)}
    mayan_view_permissions = {'POST': (permission_group_create,)}
    permission_classes = (MayanPermission,)
    queryset = Group.objects.all()
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
    queryset = Group.objects.all()
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
    queryset = get_user_model().objects.all()
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
    queryset = get_user_model().objects.all()
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
    
class APIUserGroupMap(APIView):
    """
    View to map user with groups
    
    
    **Arguments:**
        - request: Http request object.
        - pk:primary key of User

    **Returns:** User Details

    **Raises:** Nothing.

    This methods handles http POST request.

    This method map users with group.
    

    * Requires token authentication.\n
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    
    def post(self, request,pk,format=None):
        """
        Maps user with groups
        """
        groups = request.POST['group_ids'].split(',')
        userObj = User.objects.get(pk=pk)
        for group in groups:
            groupObj = Group.objects.get(pk=group)
            groupObj.user_set.add(userObj)
        mapped_group_ids = userObj.groups.all().values_list('id', flat=True)
        result = { "id":userObj.id,"groups":mapped_group_ids,"username":userObj.username,
              "fname":userObj.first_name,"lname":userObj.last_name }
        return Response({ 'data':result })
