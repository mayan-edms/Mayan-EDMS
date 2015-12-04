from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common.apps import MayanAppConfig


class NavigationApp(MayanAppConfig):
    name = 'navigation'
    test = True
    verbose_name = _('Navigation')
