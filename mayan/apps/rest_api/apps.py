from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_tools

from .links import (
    link_api, link_api_documentation, link_api_documentation_redoc
)
from .licenses import *  # NOQA


class RESTAPIApp(MayanAppConfig):
    app_url = 'api'
    name = 'rest_api'
    verbose_name = _('REST API')

    def ready(self):
        super(RESTAPIApp, self).ready()
        from .urls import api_urls

        settings.STRONGHOLD_PUBLIC_URLS += (r'^/%s/.+$' % self.app_url,)
        menu_tools.bind_links(
            links=(
                link_api, link_api_documentation, link_api_documentation_redoc
            )
        )

        for app in apps.get_app_configs():
            if getattr(app, 'has_rest_api', False):
                app_api_urls = import_string('{}.urls.api_urls'.format(app.label))
                api_urls.extend(app_api_urls)
