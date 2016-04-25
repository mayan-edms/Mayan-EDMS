from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig


class KazeApp(MayanAppConfig):
    name = 'kaze'
    verbose_name = _('Kaze')

    def ready(self):
        super(KazeApp, self).ready()
