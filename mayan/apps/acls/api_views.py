from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from mayan.apps.permissions.serializers import PermissionSerializer
from mayan.apps.rest_api import generics

from .classes import ModelPermission
from .models import AccessControlList
from .permissions import permission_acl_edit, permission_acl_view
from .serializers import (
    AccessControlListPermissionSerializer, AccessControlListSerializer,
    WritableAccessControlListPermissionSerializer,
    WritableAccessControlListSerializer
)


class APIClassPermissionList(generics.ListAPIView):
    """
    Returns a list of all the available permissions for a class.
    """
    serializer_class = PermissionSerializer

    def get_content_type(self):
        return get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

    def get_queryset(self):
        return ModelPermission.get_for_class(
            klass=self.get_content_type().model_class()
        )


class APIObjectACLListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the object's access control lists
    post: Create a new access control list for the selected object.
    """
    def get_content_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        content_object = get_object_or_404(
            klass=content_type.model_class(), pk=self.kwargs['object_id']
        )

        if self.request.method == 'GET':
            permission_required = permission_acl_view
        else:
            permission_required = permission_acl_edit

        AccessControlList.objects.check_access(
            obj=content_object, permissions=(permission_required,),
            user=self.request.user
        )

        return content_object

    def get_queryset(self):
        return self.get_content_object().acls.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIObjectACLListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'content_object': self.get_content_object(),
                }
            )

        return context

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIObjectACLListView, self).get_serializer(
            *args, **kwargs
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccessControlListSerializer
        else:
            return WritableAccessControlListSerializer


class APIObjectACLView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete the selected access control list.
    get: Returns the details of the selected access control list.
    """
    serializer_class = AccessControlListSerializer

    def get_content_object(self):
        if self.request.method == 'GET':
            permission_required = permission_acl_view
        else:
            permission_required = permission_acl_edit

        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        content_object = get_object_or_404(
            klass=content_type.model_class(), pk=self.kwargs['object_id']
        )

        AccessControlList.objects.check_access(
            obj=content_object, permissions=(permission_required,),
            user=self.request.user
        )

        return content_object

    def get_queryset(self):
        return self.get_content_object().acls.all()


class APIObjectACLPermissionListView(generics.ListCreateAPIView):
    """
    get: Returns the access control list permission list.
    post: Add a new permission to the selected access control list.
    """
    def get_acl(self):
        return get_object_or_404(
            klass=self.get_content_object().acls, pk=self.kwargs['pk']
        )

    def get_content_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        content_object = get_object_or_404(
            klass=content_type.model_class(), pk=self.kwargs['object_id']
        )

        if self.request.method == 'GET':
            permission = permission_acl_view
        else:
            permission = permission_acl_edit

        AccessControlList.objects.check_access(
            obj=content_object, permissions=(permission,),
            user=self.request.user
        )

        return content_object

    def get_queryset(self):
        return self.get_acl().permissions.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIObjectACLPermissionListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccessControlListPermissionSerializer
        else:
            return WritableAccessControlListPermissionSerializer

    def get_serializer_context(self):
        context = super(
            APIObjectACLPermissionListView, self
        ).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'acl': self.get_acl(),
                }
            )

        return context


class APIObjectACLPermissionView(generics.RetrieveDestroyAPIView):
    """
    delete: Remove the permission from the selected access control list.
    get: Returns the details of the selected access control list permission.
    """
    lookup_url_kwarg = 'permission_pk'
    serializer_class = AccessControlListPermissionSerializer

    def get_acl(self):
        return get_object_or_404(
            klass=self.get_content_object().acls, pk=self.kwargs['pk']
        )

    def get_content_object(self):
        content_type = get_object_or_404(
            klass=ContentType, app_label=self.kwargs['app_label'],
            model=self.kwargs['model_name']
        )

        content_object = get_object_or_404(
            klass=content_type.model_class(), pk=self.kwargs['object_id']
        )

        if self.request.method == 'GET':
            permission = permission_acl_view
        else:
            permission = permission_acl_edit

        AccessControlList.objects.check_access(
            obj=content_object, permissions=(permission,),
            user=self.request.user
        )

        return content_object

    def get_queryset(self):
        return self.get_acl().permissions.all()

    def get_serializer_context(self):
        context = super(
            APIObjectACLPermissionView, self
        ).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'acl': self.get_acl(),
                }
            )

        return context
