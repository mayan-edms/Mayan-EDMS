from collections import namedtuple
import io
import json

from furl import furl

from django.core.handlers.wsgi import WSGIRequest
from django.http.request import QueryDict
from django.template import Variable, VariableDoesNotExist
from django.test.client import MULTIPART_CONTENT
from django.urls import resolve
from django.urls.exceptions import Resolver404

from mayan.apps.organizations.settings import setting_organization_url_base_path
from mayan.apps.templating.classes import Template

from .literals import API_VERSION


class BatchResponse:
    def __init__(self, name, status_code, data, headers):
        self.name = name
        self.status_code = status_code
        self.data = data
        self.headers = headers


class NestableLazyIterator:
    def __init__(
        self, iterable_string, context, context_list_index, parent_iterator=None
    ):
        self.iterable_string = iterable_string
        self.context = context
        self.context_list_index = context_list_index
        self.parent_iterator = parent_iterator
        self.items = None
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Setup the initial values on the initial access.
        if not self.items:
            if self.parent_iterator:
                next(self.parent_iterator)

            self.update_iterable_object()

        if self.index == len(self.items):
            self.index = 0

            if self.parent_iterator:
                next(self.parent_iterator)
            else:
                raise StopIteration

            self.update_iterable_object()

        value = self.items[self.index]
        self.context['iterables'][self.context_list_index] = value
        self.index += 1

        return value

    def update_iterable_object(self):
        self.items = Variable(var=self.iterable_string).resolve(context=self.context)


RenderedContent = namedtuple(
    typename='RenderedContent', field_names=(
        'body', 'include', 'method', 'name', 'url'
    )
)


class BatchRequest:
    def __init__(
        self, collection, name, url, body=None, group_name=None,
        include='true', iterables=None, method='GET'
    ):
        self.collection = collection
        self.body = body or {}
        self.include = include
        self.group_name = group_name
        self.iterables = iterables
        self.method = method
        self.name = name
        self.url = url

    def execute(self):
        if self.iterables:
            # Initialize the iterables list to allow using any index.
            self.collection.context['iterables'] = [None] * len(self.iterables)

            iterator = None
            for iterable_index, iterable in enumerate(self.iterables):
                iterator = NestableLazyIterator(
                    context=self.collection.context,
                    context_list_index=iterable_index,
                    iterable_string=iterable, parent_iterator=iterator
                )

            while True:
                try:
                    next(iterator)
                except StopIteration:
                    break
                except VariableDoesNotExist as exception:
                    self.collection.responses[self.name] = {
                        'data': {'error': str(exception)},
                        'include': 'true',
                        'is_response': True
                    }
                    return
                else:
                    rendered_content = self.render_content()

                    BatchRequest(
                        collection=self.collection,
                        body=rendered_content.body,
                        group_name=self.group_name,
                        include=rendered_content.include,
                        method=rendered_content.method,
                        name=rendered_content.name,
                        url=rendered_content.url
                    ).execute()
        else:
            rendered_content = self.render_content()

            url_parts = furl(rendered_content.url)

            try:
                resolver_match = resolve(path=url_parts.pathstr)
            except Resolver404 as exception:
                self.collection.responses[rendered_content.name] = {
                    'data': {
                        'error': '"{}" not found'.format(exception.args[0]['path'])
                    },
                    'include': 'true',
                    'is_response': True,
                    'status_code': 404
                }
                return
            else:
                environ = getattr(
                    self.collection.view_request, 'environ', {}
                ).copy()

                environ['REQUEST_METHOD'] = rendered_content.method
                environ['PATH_INFO'] = self.url
                environ['QUERY_STRING'] = url_parts.querystr

                post_query_dict = QueryDict(mutable=True)
                post_query_dict.update(rendered_content.body)
                json_body = json.dumps(post_query_dict)
                request_data = json_body.encode('utf-8')
                environ['wsgi.input'] = io.BytesIO(request_data)
                environ['CONTENT_LENGTH'] = str(len(request_data))

                if rendered_content.method == 'POST':
                    environ['CONTENT_TYPE'] = MULTIPART_CONTENT
                else:
                    environ['CONTENT_TYPE'] = 'application/octet-stream'

                request = WSGIRequest(environ=environ)
                request.LANGUAGE_CODE = getattr(
                    self.collection.view_request, 'LANGUAGE_CODE', None
                )
                request.POST = post_query_dict
                request._read_started = True
                request.auth = getattr(
                    self.collection.view_request, 'auth', None
                )
                request.csrf_processing_done = True
                request.session = getattr(
                    self.collection.view_request, 'session', None
                )
                request.user = getattr(
                    self.collection.view_request, 'user', None
                )

                response = resolver_match.func(
                    request=request, **resolver_match.kwargs
                )

                result = {
                    'data': response.data,
                    'headers': {key: value for key, value in response.items()},
                    'include': rendered_content.include,
                    'is_response': True,
                    'status_code': response.status_code
                }

                self.collection.context[rendered_content.name] = result
                self.collection.responses[rendered_content.name] = result

            if self.group_name:
                self.collection.context.setdefault('groups', {})
                self.collection.context['groups'].setdefault(
                    self.group_name, []
                )
                self.collection.context['groups'][self.group_name].append(
                    result
                )

    def render_content(self):
        rendered_body = {}
        for key, value in self.body.items():
            rendered_key = Template(template_string=key).render(
                context=self.collection.context
            )
            rendered_value = Template(template_string=value).render(
                context=self.collection.context
            )
            rendered_body[rendered_key] = rendered_value

        rendered_include = Template(template_string=self.include).render(
            context=self.collection.context
        )
        rendered_method = Template(template_string=self.method).render(
            context=self.collection.context
        )
        rendered_name = Template(template_string=self.name).render(
            context=self.collection.context
        )
        rendered_url = Template(template_string=self.url).render(
            context=self.collection.context
        )

        return RenderedContent(
            body=rendered_body, include=rendered_include,
            method=rendered_method, name=rendered_name, url=rendered_url
        )


class BatchRequestCollection:
    def __init__(self, request_list=None):
        self.requests = []

        for request_index, request_dict in enumerate(request_list):
            request_dict.update(
                {'collection': self}
            )
            try:
                self.requests.append(BatchRequest(**request_dict))
            except Exception as exception:
                raise ValueError(
                    'Error instantiating request #{}; {}'.format(
                        request_index, exception
                    )
                ) from exception

    def execute(self, view_request):
        self.context = {'view_request': view_request}
        self.responses = {}
        self.view_request = view_request

        for request in self.requests:
            request.execute()

        # Convert responses in context into response class instances.
        result = []
        for key, value in self.responses.items():
            if json.loads(s=value.get('include', 'true')):
                result.append(
                    BatchResponse(
                        name=key,
                        status_code=value.get('status_code', 0),
                        data=value.get('data', {}),
                        headers=value.get('headers', {}),
                    )
                )

        return result


class Endpoint:
    def __init__(self, label, viewname=None, kwargs=None):
        self.label = label
        self.kwargs = kwargs

        if viewname:
            self.viewname = viewname
        else:
            installation_base_url = setting_organization_url_base_path.value
            if installation_base_url:
                installation_base_url = '/{}'.format(installation_base_url)
            else:
                installation_base_url = ''

            self.url = '{}/api/v{}/{}/'.format(
                installation_base_url, API_VERSION, self.label
            )

            try:
                self.viewname = resolve(path=self.url).view_name
            except Resolver404:
                self.viewname = None
