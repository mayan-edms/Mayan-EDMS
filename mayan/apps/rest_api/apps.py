from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_tools
from mayan.apps.common.settings import setting_url_base_path

from .links import (
    link_api, link_api_documentation, link_api_documentation_redoc
)


class RESTAPIApp(MayanAppConfig):
    app_url = 'api'
    app_namespace = 'rest_api'
    has_tests = True
    name = 'mayan.apps.rest_api'
    static_media_ignore_patterns = (
        'rest_framework/docs/*', 'rest_framework/img/glyphicons*',
        'rest_framework/js/*',
    )
    verbose_name = _('REST API')

    def ready(self):
        super(RESTAPIApp, self).ready()
        from .urls import api_urls

        installation_base_url = setting_url_base_path.value
        if installation_base_url:
            installation_base_url = '/{}'.format(installation_base_url)
        else:
            installation_base_url = ''

        settings.STRONGHOLD_PUBLIC_URLS += (r'^%s/api/' % installation_base_url,)

        settings.STRONGHOLD_PUBLIC_URLS += (
            r'^%s/%s/.+$' % (installation_base_url, self.app_url),
        )
        menu_tools.bind_links(
            links=(
                link_api, link_api_documentation, link_api_documentation_redoc
            )
        )

        for app in apps.get_app_configs():
            if getattr(app, 'has_rest_api', False):
                app_api_urls = import_string(dotted_path='{}.urls.api_urls'.format(app.name))
                api_urls.extend(app_api_urls)
