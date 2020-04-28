from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class LockManagerApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.lock_manager'
    verbose_name = _('Lock manager')
