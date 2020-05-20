from django.urls import resolve
from django.urls.exceptions import Resolver404

from mayan.apps.common.settings import setting_url_base_path


class Endpoint(object):
    def __init__(self, label):
        self.label = label

        installation_base_url = setting_url_base_path.value
        if installation_base_url:
            installation_base_url = '/{}'.format(installation_base_url)
        else:
            installation_base_url = ''

        url = '{}/api/{}/'.format(installation_base_url, self.label)

        try:
            self.viewname = resolve(path=url).view_name
        except Resolver404:
            self.viewname = None
