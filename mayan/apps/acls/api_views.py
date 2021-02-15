from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from mayan.apps.permissions.serializers import PermissionSerializer
from mayan.apps.rest_api.api_view_mixins import ExternalContentTypeObjectAPIViewMixin
from mayan.apps.rest_api import generics

from .classes import ModelPermission
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


class APIObjectACLListView(
    ExternalContentTypeObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the object's access control lists
    post: Create a new access control list for the selected object.
    """
    mayan_external_object_permissions = {
        'GET': (permission_acl_view,),
        'POST': (permission_acl_edit,)
    }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.external_object.acls.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'content_object': self.external_object,
                }
            )

        return context

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(
            *args, **kwargs
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccessControlListSerializer
        else:
            return WritableAccessControlListSerializer


class APIObjectACLView(
    ExternalContentTypeObjectAPIViewMixin, generics.RetrieveDestroyAPIView
):
    """
    delete: Delete the selected access control list.
    get: Returns the details of the selected access control list.
    """
    lookup_url_kwarg = 'acl_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_acl_edit,),
        'GET': (permission_acl_view,)
    }
    serializer_class = AccessControlListSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.external_object.acls.all()


class APIObjectACLPermissionListView(
    ExternalContentTypeObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns the access control list permission list.
    post: Add a new permission to the selected access control list.
    """
    mayan_external_object_permissions = {
        'GET': (permission_acl_view,),
        'POST': (permission_acl_edit,)
    }

    def get_acl(self):
        return get_object_or_404(
            klass=self.external_object.acls, pk=self.kwargs['acl_id']
        )

    def get_queryset(self):
        return self.get_acl().permissions.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccessControlListPermissionSerializer
        else:
            return WritableAccessControlListPermissionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'acl': self.get_acl(),
                }
            )

        return context


class APIObjectACLPermissionView(
    ExternalContentTypeObjectAPIViewMixin, generics.RetrieveDestroyAPIView
):
    """
    delete: Remove the permission from the selected access control list.
    get: Returns the details of the selected access control list permission.
    """
    lookup_url_kwarg = 'permission_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_acl_edit,),
        'GET': (permission_acl_view,)
    }
    serializer_class = AccessControlListPermissionSerializer

    def get_acl(self):
        return get_object_or_404(
            klass=self.external_object.acls, pk=self.kwargs['acl_id']
        )

    def get_queryset(self):
        return self.get_acl().permissions.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'acl': self.get_acl(),
                }
            )

        return context

    def perform_destroy(self, instance):
        self.get_acl().permissions_remove(
            queryset=(instance,), _user=self.request.user
        )
        instance.delete()
