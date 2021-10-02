import json

from furl import furl

from django.http.request import HttpRequest, QueryDict
from django.template import Variable, VariableDoesNotExist
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


class BatchRequest:
    def __init__(
        self, name, url, body=None, include='true', iterator=None, method='GET'
    ):
        self.body = body or {}
        self.include = include
        self.iterator = iterator
        self.method = method
        self.name = name
        self.url = url

    def execute(self, context, view_request):
        if self.iterator:
            try:
                iterator_variable = Variable(self.iterator).resolve(context=context)
            except VariableDoesNotExist as exception:
                context[self.name] = {
                    'exception': str(exception)
                }
                return
            else:
                for iterator_instance in iterator_variable:
                    iterator_instance_context = context.copy()
                    iterator_instance_context['iterator_instance'] = iterator_instance

                    rendered_body = {}
                    for key, value in self.body.items():
                        rendered_key = Template(template_string=key).render(context=iterator_instance_context)
                        rendered_value = Template(template_string=value).render(context=iterator_instance_context)
                        rendered_body[rendered_key] = rendered_value

                    # ~ rendered_body = Template(
                        # ~ template_string=self.body
                    # ~ ).render(context=iterator_instance_context)

                    rendered_include = Template(
                        template_string=self.include
                    ).render(context=iterator_instance_context)

                    rendered_method = Template(
                        template_string=self.method
                    ).render(context=iterator_instance_context)

                    rendered_name = Template(
                        template_string=self.name
                    ).render(context=iterator_instance_context)

                    rendered_url = Template(
                        template_string=self.url
                    ).render(context=iterator_instance_context)

                    BatchRequest(
                        body=rendered_body,
                        include=rendered_include,
                        method=rendered_method,
                        name=rendered_name,
                        url=rendered_url
                    ).execute(context=context, view_request=view_request)
        else:
            # ~ rendered_body = Template(
                # ~ template_string=self.body
            # ~ ).render(context=context)
            rendered_body = {}
            for key, value in self.body.items():
                rendered_key = Template(template_string=key).render(context=context)
                rendered_value = Template(template_string=value).render(context=context)
                rendered_body[rendered_key] = rendered_value

            rendered_include = Template(
                template_string=self.include
            ).render(context=context)

            rendered_method = Template(
                template_string=self.method
            ).render(context=context)

            rendered_name = Template(
                template_string=self.name
            ).render(context=context)

            rendered_url = Template(
                template_string=self.url
            ).render(context=context)

            url_parts = furl(rendered_url)
            resolver_match = resolve(path=url_parts.pathstr)

            if not resolver_match:
                raise ValueError('Invalid request URL.')

            request = HttpRequest()

            request.__dict__ = view_request.__dict__

            request.GET = view_request.GET
            request.POST = view_request.POST
            request.FILES = view_request.FILES

            request.method = rendered_method

            query_dict = getattr(view_request, request.method).copy()
            query_dict.update(QueryDict(query_string=url_parts.querystr))
            query_dict.update(rendered_body)
            setattr(request, request.method, query_dict)

            request.path = self.url
            request.path_info = self.url
            request.COOKIES = view_request.COOKIES
            request.META = view_request.META

            response = resolver_match.func(
                request=request, **resolver_match.kwargs
            )

            context[rendered_name] = {
                'data': response.data,
                'headers': {key: value for key, value in response.items()},
                'include': rendered_include,
                'status_code': response.status_code
            }


class BatchRequestCollection:
    def __init__(self, requests_list=None, requests_string=None):
        self.requests = []

        self.requests_list = requests_list
        if not requests_list:
            # Cleanup JSON string. Remove any extra line feeds and spaces.
            self.requests_list = json.loads(s=requests_string)

        for request_dict in self.requests_list:
            self.requests.append(BatchRequest(**request_dict))

    def execute(self, view_request):
        context = {'view_request': view_request}

        for request in self.requests:
            request.execute(
                context=context, view_request=view_request
            )

        # Convert accumulated context into responses.
        responses = []
        for key, value in context.items():
            if not isinstance(value, HttpRequest):
                if json.loads(s=value.get('include', 'true')):
                    responses.append(
                        BatchResponse(
                            name=key,
                            status_code=value.get('status_code', 0),
                            data=value.get('data', {}),
                            headers=value.get('headers', {}),
                        )
                    )

        return responses


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
