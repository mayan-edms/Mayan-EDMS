from rest_framework import generics as rest_framework_generics

from .filters import MayanObjectPermissionsFilter
from .mixins import (
    InstanceExtraDataAPIViewMixin, SerializerExtraContextAPIViewMixin,
    SchemaInspectionAPIViewMixin
)
from .permissions import MayanPermission


class GenericAPIView(
    SchemaInspectionAPIViewMixin, rest_framework_generics.GenericAPIView
):
    filter_backends = (MayanObjectPermissionsFilter,)
    permission_classes = (MayanPermission,)


class CreateAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, rest_framework_generics.CreateAPIView
):
    """
    requires:
        view_permission = {'POST': ...}
    """
    permission_classes = (MayanPermission,)


class ListAPIView(
    SchemaInspectionAPIViewMixin, SerializerExtraContextAPIViewMixin,
    rest_framework_generics.ListAPIView
):
    """
    requires:
        object_permission = {'GET': ...}
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    # permission_classes is required for the EventListAPIView
    # when Actions objects support ACLs then this can be removed
    # as was intented.
    permission_classes = (MayanPermission,)


class ListCreateAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin,
    rest_framework_generics.ListCreateAPIView
):
    """
    requires:
        object_permission = {'GET': ...}
        view_permission = {'POST': ...}
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    permission_classes = (MayanPermission,)


class RetrieveAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin,
    rest_framework_generics.RetrieveAPIView
):
    """
    requires:
        object_permission = {
            'GET': ...,
        }
    """
    filter_backends = (MayanObjectPermissionsFilter,)


class RetrieveDestroyAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin,
    rest_framework_generics.RetrieveDestroyAPIView
):
    """
    requires:
        object_permission = {
            'DELETE': ...,
            'GET': ...,
        }
    """
    filter_backends = (MayanObjectPermissionsFilter,)


class RetrieveUpdateAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin,
    rest_framework_generics.RetrieveUpdateAPIView
):
    """
    requires:
        object_permission = {
            'GET': ...,
            'PATCH': ...,
            'PUT': ...
        }
    """
    filter_backends = (MayanObjectPermissionsFilter,)


class RetrieveUpdateDestroyAPIView(
    SchemaInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin,
    rest_framework_generics.RetrieveUpdateDestroyAPIView
):
    """
    requires:
        object_permission = {
            'DELETE': ...,
            'GET': ...,
            'PATCH': ...,
            'PUT': ...
        }
    """
    filter_backends = (MayanObjectPermissionsFilter,)
