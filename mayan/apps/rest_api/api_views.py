from drf_yasg.views import get_schema_view

from rest_framework import permissions, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.schemas.generators import EndpointEnumerator

from mayan.apps.common.settings import setting_url_base_path

from .classes import Endpoint
from .generics import ListAPIView
from .serializers import EndpointSerializer
from .schemas import openapi_info


class APIRoot(ListAPIView):
    swagger_schema = None
    serializer_class = EndpointSerializer

    def get_queryset(self):
        """
        get: Return a list of all endpoints.
        """
        endpoint_enumerator = EndpointEnumerator()

        if setting_url_base_path.value:
            index = 3
        else:
            index = 2

        # Extract the resource names from the API endpoint URLs
        parsed_urls = []
        for entry in endpoint_enumerator.get_api_endpoints():
            parsed_urls.append(
                entry[0].split('/')[index]
            )

        parsed_urls = sorted(set(parsed_urls))

        endpoints = []
        for url in parsed_urls:
            if url:
                endpoints.append(
                    Endpoint(label=url)
                )

        return endpoints


class BrowseableObtainAuthToken(ObtainAuthToken):
    """
    Obtain an API authentication token.
    """
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer)


schema_view = get_schema_view(
    openapi_info,
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
