from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class AppearanceApp(MayanAppConfig):
    app_url = 'appearance'
    has_tests = True
    name = 'mayan.apps.appearance'
    verbose_name = _('Appearance')

    def ready(self):
        super(AppearanceApp, self).ready()
