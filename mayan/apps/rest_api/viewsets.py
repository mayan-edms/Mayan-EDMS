from __future__ import absolute_import, unicode_literals

from rest_framework import mixins, viewsets

from .filters import MayanViewSetObjectPermissionsFilter
from .mixins import SuccessHeadersMixin
from .permissions import MayanViewSetPermission


class MayanGenericAPIViewSet(SuccessHeadersMixin, viewsets.GenericViewSet):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanModelAPIViewSet(SuccessHeadersMixin, viewsets.ModelViewSet):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanReadOnlyModelAPIViewSet(
    SuccessHeadersMixin, viewsets.ReadOnlyModelViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanRetrieveUpdateAPIViewSet(
    SuccessHeadersMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)


class MayanRetrieveUpdateDestroyAPIViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    filter_backends = (MayanViewSetObjectPermissionsFilter,)
    permission_classes = (MayanViewSetPermission,)
