from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission
from rest_framework import authentication, permissions
from django.contrib.auth.models import Group, User

from .models import Role, StoredPermission
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
    
class APIMapRolePerms(APIView):
    
    """
    class based view to map Roles with permissions using APIView.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    
    def post(self, request, pk, format=None):
        """
        View to map roles with permissions
    
        **Arguments:**
            - request: Http request object.
            - pk:primary key of Role

        **Returns:** Role label with permission for respective role.

        **Raises:** Nothing.

        This methods handles http POST request.

        This method map role with permissions.
    
        * Requires token authentication.\n
        * Only admin users are able to access this view.

        """
        mapped_permission_ids=[]
        role = Role.objects.get(pk=pk)
        perms_ids = request.POST["permissions"].split(',')
        for perms_id in perms_ids:
            stored_perm = StoredPermission.objects.get(pk=perms_id)
            role.permissions.add(stored_perm)
            mapped_permission_ids.append(perms_id)
        result={"id":role.id, "label":role.label, "permission": mapped_permission_ids}
        return Response({'data':result})

class APIMapRoleGroups(APIView):
    """
     class based view to map Roles with Groups using APIView.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = RoleSerializer
    

    def post(self, request, pk, format=None):
        """
        View to map roles with group
    
        **Arguments:**
            - request: Http request object.
            - pk:primary key of Role

        **Returns:** Role label and mapped group with respective role.

        **Raises:** Nothing.

        This methods handles http POST request.

        This method map role with groups.
    
        * Requires token authentication.\n
        * Only admin users are able to access this view.

        """
        mapped_group_ids = []
        role = Role.objects.get(pk=pk)
        group_ids = request.POST["group_ids"].split(',')
        for group_id in group_ids:
            group = Group.objects.get(pk=group_id)
            role.groups.add(group)
        mapped_group_ids = role.groups.all().values_list('id', flat=True)
        result={"id":role.id, "label":role.label, "groups": mapped_group_ids}
        return Response({"data": result})

class APIDeleteRoleGroups(APIView):
    """
     class based view to delete Roles with Groups using APIView.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = RoleSerializer
    mayan_object_permissions = {'DELETE': (permission_role_delete,)}
    

    def delete(self, request, role_pk, group_pk, format=None):
        """
        View to map roles with group
    
        **Arguments:**
            - request: Http request object.
            - pk:primary key of Role

        **Returns:** Role label and mapped group with respective role.

        **Raises:** Nothing.

        This methods handles http POST request.

        This method map role with groups.
    
        * Requires token authentication.\n
        * Only admin users are able to access this view.

        """
	mapped_group_ids = []
	role = Role.objects.get(pk=role_pk)
	group = Group.objects.get(pk=group_pk)
	role.groups.remove(group)
	mapped_group_ids = role.groups.all().values_list('id', flat=True)
	result={"id":role.id, "label":role.label, "groups": mapped_group_ids}
	return Response({"data": result})


class APIGetPermission(APIView):
    """
    class based view to retrive all permissions.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request,format=None):
        """
        View to retrive all permissions.
    
        **Arguments:**
            - request: Http request object.

        **Returns:** All Id and Name of permissions.

        **Raises:** Nothing.

        This methods handles http GET request.

        This method is to retrive all permission.
    
        * Requires token authentication.\n
        * Only admin users are able to access this view.

        """
        perms = []
        queryset = StoredPermission.objects.all()
        for q in queryset:
            perms.append({'id': q.id, 'name': q.name})
        return Response({'data':perms})
