from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool

from .classes import APIEndPoint
from .links import link_api, link_api_documentation
from .urls import api_urls

endpoint = APIEndPoint('rest_api')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('auth_token_obtain', _(u'Obtain an API authentication token.'))

register_tool(link_api)
register_tool(link_api_documentation)
