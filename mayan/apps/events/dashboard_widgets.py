from django.apps import apps
from django.urls import reverse_lazy

from mayan.apps.dashboards.classes import DashboardWidgetList

from .links import link_current_user_events


class DashboardWidgetUserEvents(DashboardWidgetList):
    columns = ('event_type', 'target')
    icon = link_current_user_events.icon
    label = link_current_user_events.text
    link = reverse_lazy(
        viewname=link_current_user_events.view
    )

    def get_object_list(self):
        Action = apps.get_model(
            app_label='actstream', model_name='Action'
        )

        return Action.objects.actor(obj=self.request.user)
