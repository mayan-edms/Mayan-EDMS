from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from project_tools.api import register_tool

from .links import events_list


class EventsApp(apps.AppConfig):
    name = 'events'
    verbose_name = _('Events')

    def ready(self):
        register_tool(events_list)
