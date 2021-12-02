from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class MIMETypesApp(MayanAppConfig):
    name = 'mayan.apps.mime_types'
    has_tests = True
    verbose_name = _('MIME types')

    def ready(self, *args, **kwargs):
        super().ready(*args, **kwargs)
