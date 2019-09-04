from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, patch_cache_control

from rest_framework import generics

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api.filters import MayanObjectPermissionsFilter
from mayan.apps.rest_api.permissions import MayanPermission

from .literals import CONTROL_SHEET_CODE_IMAGE_TASK_TIMEOUT
from .models import ControlSheet
from .permissions import (
    permission_control_sheet_create, permission_control_sheet_delete,
    permission_control_sheet_edit, permission_control_sheet_view
)
from .serializers import (
    ControlSheetSerializer, ControlSheetCodeSerializer
)

from .settings import settings_control_sheet_code_image_cache_time
from .tasks import task_generate_control_sheet_code_image


class ControlSheetAPIViewMixin(object):
    def get_control_sheet(self):
        if self.request.method == 'GET':
            permission = permission_control_sheet_view
        else:
            permission = permission_control_sheet_edit

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=ControlSheet.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['control_sheet_id']
        )


class APIControlSheetListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the control sheets.
    post: Create a new control sheet.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_control_sheet_view,)}
    mayan_view_permissions = {'POST': (permission_control_sheet_create,)}
    permission_classes = (MayanPermission,)
    queryset = ControlSheet.objects.all()
    serializer_class = ControlSheetSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIControlSheetListView, self).get_serializer(
            *args, **kwargs
        )


class APIControlSheetView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected control sheet.
    get: Return the details of the selected control sheet.
    patch: Edit the selected control sheet.
    put: Edit the selected control sheet.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'DELETE': (permission_control_sheet_delete,),
        'GET': (permission_control_sheet_view,),
        'PATCH': (permission_control_sheet_edit,),
        'PUT': (permission_control_sheet_edit,)
    }
    lookup_url_kwarg = 'control_sheet_id'
    queryset = ControlSheet.objects.all()
    serializer_class = ControlSheetSerializer

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIControlSheetView, self).get_serializer(
            *args, **kwargs
        )


class APIControlSheetCodeListView(
    ControlSheetAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the control sheet codes.
    post: Create a new control sheet code.
    """
    serializer_class = ControlSheetCodeSerializer

    def get_queryset(self):
        return self.get_control_sheet().codes.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(
            APIControlSheetCodeListView, self
        ).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'control_sheet': self.get_control_sheet(),
                }
            )

        return context


class APIControlSheetCodeView(
    ControlSheetAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected control sheet code.
    get: Return the details of the selected control sheet code.
    patch: Edit the selected control sheet code.
    put: Edit the selected control sheet code.
    """
    lookup_url_kwarg = 'control_sheet_code_id'
    serializer_class = ControlSheetCodeSerializer

    def get_queryset(self):
        return self.get_control_sheet().codes.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIControlSheetCodeView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'control_sheet': self.get_control_sheet(),
                }
            )

        return context


class APIControlSheetCodeImageView(
    ControlSheetAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected control_sheet.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    lookup_url_kwarg = 'control_sheet_code_id'

    def get_queryset(self):
        return self.get_control_sheet().codes.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    @cache_control(private=True)
    def retrieve(self, request, *args, **kwargs):
        task = task_generate_control_sheet_code_image.apply_async(
            kwargs=dict(
                control_sheet_code_id=self.get_object().pk,
            )
        )

        cache_filename = task.get(timeout=CONTROL_SHEET_CODE_IMAGE_TASK_TIMEOUT)
        cache_file = self.get_object().cache_partition.get_file(filename=cache_filename)
        with cache_file.open() as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response,
                    max_age=settings_control_sheet_code_image_cache_time.value
                )
            return response
