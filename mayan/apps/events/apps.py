from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_tools

from navigation import SourceColumn

from .links import link_events_list
from .licenses import *  # NOQA
from .widgets import event_type_link


class EventsApp(MayanAppConfig):
    name = 'events'
    test = True
    verbose_name = _('Events')

    def ready(self):
        super(EventsApp, self).ready()
        Action = apps.get_model(app_label='actstream', model_name='Action')

        SourceColumn(
            source=Action, label=_('Timestamp'), attribute='timestamp'
        )
        SourceColumn(source=Action, label=_('Actor'), attribute='actor')
        SourceColumn(
            source=Action, label=_('Verb'),
            func=lambda context: event_type_link(context['object'])
        )

        menu_tools.bind_links(links=(link_events_list,))
