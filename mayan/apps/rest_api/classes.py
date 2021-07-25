from django.urls import resolve
from django.urls.exceptions import Resolver404

from mayan.apps.organizations.settings import setting_organization_url_base_path

from .literals import API_VERSION


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
