import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

logger = logging.getLogger(name=__name__)


class OrganizationsApp(MayanAppConfig):
    app_namespace = 'organizations'
    app_url = 'organizations'
    name = 'mayan.apps.organizations'
    verbose_name = _('Organizations')

    def ready(self):
        super().ready()
