from rest_framework import generics

from .filters import MayanObjectPermissionsFilter
from .mixins import (
    InstanceExtraDataAPIViewMixin, SerializerExtraContextAPIViewMixin
)
from .permissions import MayanPermission




class GenericAPIView(SerializerInspectionAPIViewMixin, generics.GenericAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    permission_classes = (MayanPermission,)


class ListAPIView(
    SerializerInspectionAPIViewMixin, SerializerExtraContextAPIViewMixin,
    generics.ListAPIView
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
    SerializerInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, generics.ListCreateAPIView
):
    """
    requires:
        object_permission = {'GET': ...}
        view_permission = {'POST': ...}
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    permission_classes = (MayanPermission,)


class RetrieveAPIView(
    SerializerInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, generics.RetrieveAPIView
):
    """
    requires:
        object_permission = {
            'GET': ...,
        }
    """
    filter_backends = (MayanObjectPermissionsFilter,)


class RetrieveDestroyAPIView(
    SerializerInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, generics.RetrieveDestroyAPIView
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
    SerializerInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, generics.RetrieveUpdateAPIView
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
    SerializerInspectionAPIViewMixin, InstanceExtraDataAPIViewMixin,
    SerializerExtraContextAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
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
