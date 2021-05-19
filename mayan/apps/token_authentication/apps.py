import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

logger = logging.getLogger(name=__name__)


class TokenAuthenticationApp(MayanAppConfig):
    app_namespace = 'token_authentication'
    app_url = 'token_authentication'
    has_tests = False
    name = 'mayan.apps.token_authentication'
    verbose_name = _('Token authentication')

    def ready(self):
        super().ready()
