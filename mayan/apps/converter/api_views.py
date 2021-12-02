import logging

from django.http import HttpResponse

from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalContentTypeObjectAPIViewMixin

from .api_view_mixins import APIImageViewMixin
from .classes import AppImageErrorImage
from .models import Asset
from .permissions import (
    permission_asset_create, permission_asset_delete, permission_asset_edit,
    permission_asset_view
)
from .serializers import AssetSerializer

logger = logging.getLogger(name=__name__)


class APIAssetListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the assets.
    post: Create a new asset.
    """
    mayan_object_permissions = {'GET': (permission_asset_view,)}
    mayan_view_permissions = {'POST': (permission_asset_create,)}
    ordering_fields = ('id', 'internal_name', 'label')
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


class APIAssetImageView(APIImageViewMixin, generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected document.
    """
    lookup_url_kwarg = 'asset_id'
    mayan_object_permissions = {
        'GET': (permission_asset_view,),
    }
    queryset = Asset.objects.all()


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
            response = HttpResponse(content=file_object.read(), content_type='image')
            return response


class APIContentObjectImageView(
    APIImageViewMixin, ExternalContentTypeObjectAPIViewMixin,
    generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected content object.
    """
    def get_content_type(self):
        return self.content_type

    def set_object(self):
        self.obj = self.external_object
