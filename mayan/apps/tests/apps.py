from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class TestsApp(MayanAppConfig):
    name = 'mayan.apps.tests'
    verbose_name = _('Tests')

    def ready(self, *args, **kwargs):
        super(TestsApp, self).ready(*args, **kwargs)
