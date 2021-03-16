from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory

from .icons import (
    icon_current_user_events, icon_current_user_events_export,
    icon_event_types_subscriptions_list, icon_events_for_object,
    icon_events_for_object_export, icon_events_list,
    icon_events_list_export, icon_notification_mark_read,
    icon_notification_mark_read_all,
    icon_object_event_types_user_subcriptions_list,
    icon_user_notifications_list
)
from .permissions import permission_events_view


def get_unread_notification_count(context):
    Notification = apps.get_model(
        app_label='events', model_name='Notification'
    )
    if context.request.user.is_authenticated:
        return Notification.objects.filter(
            user=context.request.user
        ).filter(read=False).count()


link_current_user_events = Link(
    icon=icon_current_user_events, text=_('My events'),
    view='events:current_user_events'
)
link_current_user_events_export = Link(
    icon=icon_current_user_events_export, text=_('Export events'),
    view='events:current_user_events_export'
)
link_events_details = Link(
    text=_('Events'), view='events:events_list'
)
link_events_for_object = Link(
    icon=icon_events_for_object,
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_events_view,), text=_('Events'),
    view='events:events_for_object'
)
link_events_for_object_export = Link(
    icon=icon_events_for_object_export,
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_events_view,), text=_('Export events'),
    view='events:events_for_object_export'
)
link_events_list = Link(
    icon=icon_events_list, text=_('Events'), view='events:events_list'
)
link_events_list_export = Link(
    icon=icon_events_list_export, text=_('Export events'),
    view='events:events_list_export'
)
link_event_types_subscriptions_list = Link(
    icon=icon_event_types_subscriptions_list,
    text=_('Event subscriptions'),
    view='events:event_types_user_subcriptions_list'
)
link_notification_mark_read = Link(
    args='object.pk', icon=icon_notification_mark_read,
    text=_('Mark as seen'), view='events:notification_mark_read'
)
link_notification_mark_read_all = Link(
    icon=icon_notification_mark_read_all, text=_('Mark all as seen'),
    view='events:notification_mark_read_all'
)
link_object_event_types_user_subcriptions_list = Link(
    icon=icon_object_event_types_user_subcriptions_list,
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_events_view,), text=_('Subscriptions'),
    view='events:object_event_types_user_subcriptions_list',
)
link_user_notifications_list = Link(
    badge_text=get_unread_notification_count,
    icon=icon_user_notifications_list, text='',
    view='events:user_notifications_list'
)
