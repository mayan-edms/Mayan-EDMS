from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class ImporterApp(MayanAppConfig):
    app_namespace = 'importer'
    app_url = 'importer'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.importer'
    verbose_name = _('Importer')

    def ready(self):
        super(ImporterApp, self).ready()
