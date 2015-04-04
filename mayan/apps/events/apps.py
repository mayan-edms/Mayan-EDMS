from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_tools

from .links import link_events_list


class EventsApp(apps.AppConfig):
    name = 'events'
    verbose_name = _('Events')

    def ready(self):
        menu_tools.bind_links(links=[link_events_list])
