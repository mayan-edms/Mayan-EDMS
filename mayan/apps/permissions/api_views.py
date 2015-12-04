from __future__ import unicode_literals

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Role
from .permissions import (
    permission_role_create, permission_role_delete, permission_role_edit,
    permission_role_view
)
from .serializers import RoleSerializer


class APIRoleListView(generics.ListCreateAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_role_view,)}
    mayan_view_permissions = {'POST': (permission_role_create,)}

    def get(self, *args, **kwargs):
        """
        Returns a list of all the roles.
        """

        return super(APIRoleListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new role.
        """

        return super(APIRoleListView, self).post(*args, **kwargs)


class APIRoleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': (permission_role_view,),
        'PUT': (permission_role_edit,),
        'PATCH': (permission_role_edit,),
        'DELETE': (permission_role_delete,)
    }

    def delete(self, *args, **kwargs):
        """
        Delete the selected role.
        """

        return super(APIRoleView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected role.
        """

        return super(APIRoleView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the selected role.
        """

        return super(APIRoleView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected role.
        """

        return super(APIRoleView, self).put(*args, **kwargs)
