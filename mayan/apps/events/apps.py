from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_tools

from .links import link_events_list


class EventsApp(MayanAppConfig):
    name = 'events'
    verbose_name = _('Events')

    def ready(self):
        super(EventsApp, self).ready()

        menu_tools.bind_links(links=[link_events_list])
