import copy
import json

from furl import furl
from drf_yasg.views import get_schema_view

from django.http.request import QueryDict
from django.template import Variable, VariableDoesNotExist

from rest_framework import permissions, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.schemas.generators import EndpointEnumerator

from rest_framework import serializers

import mayan
from mayan.apps.organizations.settings import setting_organization_url_base_path
from mayan.apps.templating.classes import Template
from mayan.apps.rest_api import generics
from mayan.apps.views.utils import resolve

from .classes import Endpoint
from .generics import RetrieveAPIView, ListAPIView
from .serializers import EndpointSerializer, ProjectInformationSerializer
from .schemas import openapi_info


class APIRoot(ListAPIView):
    swagger_schema = None
    serializer_class = EndpointSerializer

    def get_queryset(self):
        """
        get: Return a list of all API root endpoints. This includes the
        API version root and root services.
        """
        endpoint_api_version = Endpoint(
            label='API version root', viewname='rest_api:api_version_root'
        )
        endpoint_redoc = Endpoint(
            label='ReDoc UI', viewname='rest_api:schema-redoc'
        )
        endpoint_swagger = Endpoint(
            label='Swagger UI', viewname='rest_api:schema-swagger-ui'
        )
        endpoint_swagger_schema_json = Endpoint(
            label='API schema (JSON)', viewname='rest_api:schema-json',
            kwargs={'format': '.json'}
        )
        endpoint_swagger_schema_yaml = Endpoint(
            label='API schema (YAML)', viewname='rest_api:schema-json',
            kwargs={'format': '.yaml'}
        )
        return [
            endpoint_api_version,
            endpoint_swagger,
            endpoint_redoc,
            endpoint_swagger_schema_json,
            endpoint_swagger_schema_yaml
        ]


class APIVersionRoot(ListAPIView):
    swagger_schema = None
    serializer_class = EndpointSerializer

    def get_queryset(self):
        """
        get: Return a list of the API version resources and endpoint.
        """
        endpoint_enumerator = EndpointEnumerator()

        if setting_organization_url_base_path.value:
            url_index = 4
        else:
            url_index = 3

        # Extract the resource names from the API endpoint URLs
        parsed_urls = set()
        for entry in endpoint_enumerator.get_api_endpoints():
            try:
                url = entry[0].split('/')[url_index]
            except IndexError:
                """An unknown or invalid URL"""
            else:
                parsed_urls.add(url)

        endpoints = []
        for url in sorted(parsed_urls):
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


class ProjectInformationAPIView(RetrieveAPIView):
    serializer_class = ProjectInformationSerializer

    def get_object(self):
        return mayan


class BatchRequest:
    def __init__(self, requests):
        self.requests = requests

    def _execute_request(self, context, request):
        result = context.copy()

        if request.get('iterator'):
            for instance_index, instance in enumerate(Variable(request.get('iterator')).resolve(context=result)):
                temp_context = result.copy()
                temp_context['iterator_instance'] = instance

                rendered_url = Template(request['url']).render(context=temp_context)
                rendered_name = Template(request['name']).render(context=temp_context)

                sub_request = {
                    'url': rendered_url,
                    'name': rendered_name
                }
                result.update(
                    self._execute_request(context=result, request=sub_request)
                )
        else:
            method = request.get('method', 'GET')
            url_parts = furl(request['url'])

            resolved_match = resolve(path=str(url_parts.path))

            serializer_request = copy.copy(self.serializer.context['request']._request)
            serializer_request.method = method
            setattr(serializer_request, method, QueryDict(str(url_parts.query)))
            serializer_request.path = request['url']

            response = resolved_match.func(
                request=serializer_request, **resolved_match.kwargs
            )
            result[request['name']] = response.data

        return result

    def execute(self, serializer):
        context = {}
        requests = json.loads(self.requests)
        self.serializer = serializer

        for request in requests:
            context.update(
                self._execute_request(
                    context=context, request=request
                )
            )

        return context


class BatchAPIRequestSerializer(serializers.Serializer):
    requests = serializers.CharField()

    def create(self, validated_data):
        test_batch_requests = '''
        [
            {"url": "/api/v4/search/documents.DocumentSearchResult/?label=8b3332489", "name": "document_list"},
            {
                "iterator": "document_list.results",
                "url": "/api/v4/documents/{{ iterator_instance.id }}/metadata/",
                "name": "document_metadata_{{ iterator_instance.id }}"
            }
        ]
        '''
        batch_request = BatchRequest(requests=test_batch_requests)
        result = batch_request.execute(serializer=self)

        breakpoint()
        return batch_request


class BatchRequestAPIView(generics.CreateAPIView):
    """
    post: Create a batch API request.
    """
    serializer_class = BatchAPIRequestSerializer


schema_view = get_schema_view(
    info=openapi_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    validators=['flex', 'ssv']
)
