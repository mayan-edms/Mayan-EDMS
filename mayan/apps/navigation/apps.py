from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class NavigationApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.navigation'
    verbose_name = _('Navigation')
