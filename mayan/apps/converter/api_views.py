import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_control, patch_cache_control

from mayan.apps.rest_api import generics

from .classes import AppImageErrorImage
from .literals import ASSET_IMAGE_TASK_TIMEOUT
from .models import Asset
from .permissions import (
    permission_asset_create, permission_asset_delete, permission_asset_edit,
    permission_asset_view
)
from .serializers import AssetSerializer
from .settings import setting_asset_cache_time
from .tasks import task_asset_image_generate

logger = logging.getLogger(name=__name__)


class APIAssetListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the assets.
    post: Create a new asset.
    """
    mayan_object_permissions = {'GET': (permission_asset_view,)}
    mayan_view_permissions = {'POST': (permission_asset_create,)}
    ordering_fields = ('internal_name', 'label')
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIAssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected asset.
    get: Return the details of the selected asset.
    patch: Edit the properties of the selected asset.
    put: Edit the properties of the selected asset.
    """
    lookup_url_kwarg = 'asset_id'
    mayan_object_permissions = {
        'DELETE': (permission_asset_delete,),
        'GET': (permission_asset_view,),
        'PATCH': (permission_asset_edit,),
        'PUT': (permission_asset_edit,)
    }
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIAssetImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document.
    """
    lookup_url_kwarg = 'asset_id'
    mayan_object_permissions = {
        'GET': (permission_asset_view,),
    }
    queryset = Asset.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    @cache_control(private=True)
    def retrieve(self, request, *args, **kwargs):
        task = task_asset_image_generate.apply_async(
            kwargs={
                'asset_id': self.get_object().pk,
            }
        )

        kwargs = {'timeout': ASSET_IMAGE_TASK_TIMEOUT}
        if settings.DEBUG:
            # In debug more, task are run synchronously, causing this method
            # to be called inside another task. Disable the check of nested
            # tasks when using debug mode.
            kwargs['disable_sync_subtasks'] = False

        cache_filename = task.get(**kwargs)
        cache_file = self.get_object().cache_partition.get_file(
            filename=cache_filename
        )
        with cache_file.open() as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response=response,
                    max_age=setting_asset_cache_time.value
                )
            return response


class APIAppImageErrorImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected app image error.
    """
    lookup_url_kwarg = 'app_image_error_name'

    def get_object(self):
        return AppImageErrorImage.get(
            name=self.kwargs[self.lookup_url_kwarg]
        )

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def retrieve(self, request, *args, **kwargs):
        with self.get_object().open() as file_object:
            response = HttpResponse(file_object.read(), content_type='image')
            return response
