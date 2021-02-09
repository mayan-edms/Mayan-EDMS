from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class PlatformApp(MayanAppConfig):
    app_namespace = 'platform'
    app_url = 'platform'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.platform'
    verbose_name = _('Platform')

    def ready(self):
        super().ready()
