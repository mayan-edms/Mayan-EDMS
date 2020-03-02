from __future__ import absolute_import, unicode_literals

from rest_framework import mixins, viewsets

from .filters import MayanViewSetObjectPermissionsFilter
from .mixins import SerializerExtraContextMixin, SuccessHeadersMixin
from .permissions import MayanViewSetPermission


class MayanCreateDestroyListRetrieveAPIViewSet(
    SuccessHeadersMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanDestroyListRetrieveUpdateAPIViewSet(
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanGenericAPIViewSet(SuccessHeadersMixin, viewsets.GenericViewSet):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanListRetrieveUpdateAPIViewSet(
    SuccessHeadersMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanModelAPIViewSet(
    SerializerExtraContextMixin, SuccessHeadersMixin, viewsets.ModelViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanReadOnlyModelAPIViewSet(
    SuccessHeadersMixin, viewsets.ReadOnlyModelViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)
