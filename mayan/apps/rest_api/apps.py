from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool

from .classes import APIEndPoint
from .links import link_api, link_api_documentation


class RESTAPIApp(apps.AppConfig):
    name = 'rest_api'
    verbose_name = _('REST API')

    def ready(self):
        APIEndPoint('rest_api')

        register_tool(link_api)
        register_tool(link_api_documentation)
