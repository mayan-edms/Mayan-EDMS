from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class MIMETypesApp(MayanAppConfig):
    name = 'mayan.apps.mimetype'
    has_tests = True
    verbose_name = _('MIME types')

    def ready(self, *args, **kwargs):
        super(MIMETypesApp, self).ready(*args, **kwargs)
