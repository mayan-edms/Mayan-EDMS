from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.signals import post_initial_setup, post_upgrade

from .handlers import handler_install_javascript


class DependenciesApp(MayanAppConfig):
    app_namespace = 'dependencies'
    app_url = 'dependencies'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.dependencies'
    verbose_name = _('Dependencies')

    def ready(self):
        super(DependenciesApp, self).ready()

        post_initial_setup.connect(
            dispatch_uid='dependendies_handler_install_javascript',
            receiver=handler_install_javascript
        )
        post_upgrade.connect(
            dispatch_uid='dependendies_handler_install_javascript',
            receiver=handler_install_javascript
        )
