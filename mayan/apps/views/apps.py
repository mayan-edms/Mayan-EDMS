import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

logger = logging.getLogger(name=__name__)


class ViewsApp(MayanAppConfig):
    app_namespace = 'views'
    app_url = 'views'
    has_tests = True
    name = 'mayan.apps.views'
    verbose_name = _('Views')

    def ready(self):
        super().ready()
