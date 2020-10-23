from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class TestingApp(MayanAppConfig):
    name = 'mayan.apps.testing'
    verbose_name = _('Testing')

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)
