from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from actstream.models import Action

from common import MayanAppConfig, menu_tools
from common.utils import encapsulate
from navigation import SourceColumn

from .links import link_events_list
from .widgets import event_type_link


class EventsApp(MayanAppConfig):
    name = 'events'
    verbose_name = _('Events')

    def ready(self):
        super(EventsApp, self).ready()

        SourceColumn(source=Action, label=_('Timestamp'), attribute='timestamp')
        SourceColumn(source=Action, label=_('Actor'), attribute='actor')
        SourceColumn(source=Action, label=_('Verb'), attribute=encapsulate(
            lambda entry: event_type_link(entry))
        )

        menu_tools.bind_links(links=[link_events_list])
