from __future__ import unicode_literals

from project_tools.api import register_tool

from .classes import APIEndPoint
from .links import link_api, link_api_documentation

APIEndPoint('rest_api')

register_tool(link_api)
register_tool(link_api_documentation)
