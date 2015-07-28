from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_tools

from .classes import APIEndPoint
from .links import link_api, link_api_documentation


class RESTAPIApp(apps.AppConfig):
    name = 'rest_api'
    verbose_name = _('REST API')

    def ready(self):
        APIEndPoint('rest_api')

        menu_tools.bind_links(links=(link_api, link_api_documentation))
