from __future__ import unicode_literals

from django.apps import apps
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_object, menu_secondary, menu_tools, menu_topbar, menu_user
)
from mayan.apps.navigation.classes import SourceColumn

from .handlers import handler_create_system_user
from .html_widgets import (
    ObjectLinkWidget, widget_event_actor_link, widget_event_type_link
)
from .links import (
    link_current_user_events, link_event_types_subscriptions_list,
    link_events_list, link_notification_mark_read,
    link_notification_mark_read_all, link_user_notifications_list,
)


class EventsApp(MayanAppConfig):
    app_namespace = 'events'
    app_url = 'events'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.events'
    verbose_name = _('Events')

    def ready(self):
        super(EventsApp, self).ready()
        Action = apps.get_model(app_label='actstream', model_name='Action')
        Notification = self.get_model(model_name='Notification')
        StoredEventType = self.get_model(model_name='StoredEventType')

        # Add labels to Action model, they are not marked translatable in the
        # upstream package.
        SourceColumn(
            attribute='timestamp', is_identifier=True,
            is_sortable=True, label=_('Date and time'), source=Action
        )
        SourceColumn(
            func=widget_event_actor_link, label=_('Actor'), source=Action
        )
        SourceColumn(
            func=widget_event_type_link, label=_('Event'), source=Action
        )
        SourceColumn(
            attribute='target', label=_('Target'), source=Action,
            widget=ObjectLinkWidget
        )
        SourceColumn(
            attribute='action_object', label=_('Action object'), source=Action,
            widget=ObjectLinkWidget
        )

        SourceColumn(
            source=StoredEventType, label=_('Namespace'), attribute='namespace'
        )
        SourceColumn(
            source=StoredEventType, label=_('Label'), attribute='label'
        )

        SourceColumn(
            attribute='action__timestamp', is_identifier=True,
            is_sortable=True, label=_('Date and time'), source=Notification
        )
        SourceColumn(
            func=widget_event_actor_link, label=_('Actor'),
            kwargs={'attribute': 'action'}, source=Notification
        )
        SourceColumn(
            func=widget_event_type_link, label=_('Event'),
            kwargs={'attribute': 'action'}, source=Notification
        )
        SourceColumn(
            attribute='action.target', label=_('Target'), source=Notification,
            widget=ObjectLinkWidget
        )

        SourceColumn(
            attribute='read', is_sortable=True, label=_('Seen'),
            source=Notification, widget=TwoStateWidget
        )

        menu_topbar.bind_links(
            links=(link_user_notifications_list,), position=99
        )
        menu_object.bind_links(
            links=(link_notification_mark_read,), sources=(Notification,)
        )
        menu_secondary.bind_links(
            links=(link_notification_mark_read_all,),
            sources=('events:user_notifications_list',)
        )
        menu_tools.bind_links(links=(link_events_list,))
        menu_user.bind_links(
            links=(
                link_event_types_subscriptions_list, link_current_user_events
            ), position=50
        )

        post_migrate.connect(
            dispatch_uid='events_create_system_user',
            receiver=handler_create_system_user,
        )
